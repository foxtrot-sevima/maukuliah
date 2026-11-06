"""
Turn a raw "Save As > Webpage, Complete" outerHTML capture into a clean,
static mockup that is wired to the QUANTUM design system, plus a manifest
report showing which QUANTUM tokens/components were used (and what wasn't
found in the local QUANTUM copy).

Pages are grouped one folder per MODULE, not one folder per page - all pages
belonging to the same module (e.g. every "kerjasama" screen) share a single
folder and a single copy of the vendored CSS/JS/fonts (`_assets/`), since
that's always the exact same QUANTUM/app bundle regardless of which page it's
attached to. There's nothing to `npm install` here - QUANTUM is a private
package (`@quantum/web`, hosted on SEVIMA's internal GitLab, not any
registry this environment can reach) - vendoring a local copy is the only
offline-friendly option, this just avoids doing it once per page.

Usage:
    python mockups/scripts/build_mockup.py <path-to-raw-html> [module[/page]]

    <path-to-raw-html>  Absolute path, or a path relative to mockups/raw/
    [module[/page]]     Where to put the output: mockups/pages/<module>/<page>.html
                         - "kerjasama/daftar" -> mockups/pages/kerjasama/daftar.html
                         - "dashboard" (no slash) -> mockups/pages/dashboard/index.html
                         Defaults to a slugified version of the html filename
                         (as a single-segment module, page "index").

Example:
    python mockups/scripts/build_mockup.py "raw/kerjasama-daftar/Daftar Kerjasama.html" kerjasama/daftar
"""
import json
import os
import re
import shutil
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup, Comment

ROOT = Path(__file__).resolve().parents[2]
MOCKUPS = ROOT / "mockups"
TOKENS_DIR = MOCKUPS / "tokens"
PAGES_DIR = MOCKUPS / "pages"
# Hand-supplied real assets (e.g. the actual hero images, not the tiny
# blur-up placeholder a lazy-load pattern leaves in the capture's own local
# src) - checked ahead of the capture's own copy for any filename that
# matches, across every module.
CURATED_ASSETS_DIR = MOCKUPS / "assets"
ROUTE_MAP_PATH = PAGES_DIR / "route-map.json"

# The most current Bootstrap+Quantum bundle available in the local QUANTUM
# checkout. Update this if QUANTUM ships a newer assets/release/*.css.
QUANTUM_LIVE_CSS = ROOT / "QUANTUM" / "quantum" / "assets" / "release" / "app-20230510001.css"
QUANTUM_ASSET_ROOT = ROOT / "QUANTUM" / "quantum"  # root that leading "/assets/..." urls resolve against
QUANTUM_V34 = ROOT / "QUANTUM" / "quantum-ai" / "source" / "quantum-v3.4"
QUANTUM_ICONS = QUANTUM_ASSET_ROOT / "assets" / "fonts" / "Icons"
QUANTUM_INSTRUMENT_SANS = ROOT / "QUANTUM" / "pwa-laravel" / "public" / "fonts" / "InstrumentSans" / "fonts" / "webfonts"

# Assets production references by a hashed/versioned filename that the browser
# capture never saved (e.g. Vite build output). Matched by prefix+suffix so
# the hash doesn't matter, then copied from this *local, first-party* source
# instead of ever touching the network. Everything here must stay offline.
KNOWN_LOCAL_ASSETS = [
    ("quantum-symbols", ".woff2", QUANTUM_V34 / "quantum-symbols" / "font" / "fonts" / "quantum-symbols.woff2"),
    ("quantum-symbols", ".woff", QUANTUM_V34 / "quantum-symbols" / "font" / "fonts" / "quantum-symbols.woff"),
    ("sevima-header", ".webp", QUANTUM_V34 / "quantum-web" / "assets" / "patterns" / "sevima-header.webp"),
    ("sevima-sidebar", ".svg", QUANTUM_V34 / "quantum-web" / "assets" / "patterns" / "sevima-sidebar.svg"),
    # "sevima-icons" (core.css @font-face) drives modal header icons, dropdown
    # "selected" checkmarks, pagination arrows, and form clear/show-password
    # icons - referenced by a *relative* url() in the capture (`./../../assets/
    # fonts/Icons/...`) that never resolves once the CSS moves into
    # _assets/captured/, and the actual font binaries are never part of a
    # browser capture in the first place - so always resolve from QUANTUM.
    ("sevima-icons", ".eot", QUANTUM_ICONS / "sevima-icons.eot"),
    ("sevima-icons", ".ttf", QUANTUM_ICONS / "sevima-icons.ttf"),
    ("sevima-icons", ".woff", QUANTUM_ICONS / "sevima-icons.woff"),
    ("sevima-icons", ".svg", QUANTUM_ICONS / "sevima-icons.svg"),
    # Google Fonts "Instrument Sans" (css2.css @font-face, the app's body
    # font) - browser captures never save the actual woff2 binaries for
    # fonts.gstatic.com, only the referencing CSS, so every hashed filename
    # Google currently serves for this family is pinned here explicitly
    # (2 weights/styles x {latin, latin-ext} subset = 4 filenames, all
    # resolving to the same 2 local variable-font files QUANTUM already
    # bundles). Update this if Google reissues the font under new hashes.
    ("pxiTypc9vsFDm051Uf6KVwgkfoSxQ0GsQv8ToedPibnr0She1YmV", ".woff2",
     QUANTUM_INSTRUMENT_SANS / "InstrumentSans[wdth,wght].woff2"),  # normal, latin-ext
    ("pxiTypc9vsFDm051Uf6KVwgkfoSxQ0GsQv8ToedPibnr0SZe1Q", ".woff2",
     QUANTUM_INSTRUMENT_SANS / "InstrumentSans[wdth,wght].woff2"),  # normal, latin
    ("pxitypc9vsFDm051Uf6KVwgkfoSbSnNPooZAN0lInHGpCWNu2ZGRu3k", ".woff2",
     QUANTUM_INSTRUMENT_SANS / "InstrumentSans-Italic[wdth,wght].woff2"),  # italic, latin-ext
    ("pxitypc9vsFDm051Uf6KVwgkfoSbSnNPooZAN0lInHGpCWNu15GR", ".woff2",
     QUANTUM_INSTRUMENT_SANS / "InstrumentSans-Italic[wdth,wght].woff2"),  # italic, latin
]

# External <script src> the capture saved under a hashed/generic filename -
# functional and fully self-contained (verified: no further imports), so
# they're restored under a clean local name instead of being dropped like
# the rest of the capture's scripts.
FUNCTIONAL_SCRIPTS = [
    ("chart.umd.js.download", "chart.js"),
    ("chartjs-plugin-datalabels.min.js.download", "chartjs-plugin-datalabels.min.js"),
    ("chart-settings.js.download", "chart-settings.js"),
    # Livewire v3 ships Alpine.js bundled inside itself (verified: fully
    # self-contained, no further imports, `window.Alpine` assigned) - pages
    # built on this design system drive sidebar submenus, dropdowns opened
    # via x-on:click, and modal content population purely through Alpine
    # directives (x-data/x-show/x-on/$dispatch), so restoring the real,
    # captured Livewire bundle (not a hand-rolled shim) is what actually
    # makes those directives work, identically to production.
    ("livewire.min.js.download", "livewire.min.js"),
    # Shared framework bundle (verified self-contained, no imports) - among
    # other small utilities, this is where the site's lazy-load image engine
    # lives (class="lazy", data-src -> src swap, "entered"/"loaded" state
    # classes, data-ll-status). Without it, any <img class="lazy" data-src=
    # "..."> with no src of its own (a common pattern here, not just a rare
    # edge case) never gets its real image assigned at all - it just sits
    # invisible/blank forever, which is exactly what looked like a missing
    # hero image / stuck loading state.
    ("app-BbkPvvSm.js.download", "app.js"),
    # Selectize (jQuery-plugin build) turns a plain <select> into a
    # searchable multi-select box - the <select> itself is always still in
    # the capture (just CSS-hidden, `style="display:none"`), but nothing
    # replaces it with the real widget unless this JS actually runs, so
    # without it the filter is neither the fancy widget NOR a working plain
    # dropdown - just an inert, invisible <select>. Both files verified
    # self-contained (no further imports); jQuery must load before Selectize
    # (it's a jQuery plugin) - script tag order in the capture already has
    # jQuery first, and restore_functional_scripts preserves document order.
    ("jquery.min.js.download", "jquery.min.js"),
    ("selectize.min.js.download", "selectize.min.js"),
]
# Inline <script> is only kept if its content matches one of these - avoids
# hand-picking index positions, which shift between captures.
FUNCTIONAL_INLINE_SCRIPT_SIGNATURES = (
    "Chart.register(ChartDataLabels)",
    # This app's own charts don't use the datalabels plugin at all - just
    # plain `new Chart(el, {...})` with the real per-page data inline. The
    # signature above never matches here, so without this the chart-init
    # script (and the only place the chart's real data lives) was being
    # stripped as noise like any other inline script, leaving an empty
    # <canvas> - chart.js itself was vendored and loading for nothing.
    "new Chart(",
    # Public-site navbar: hidden (opacity-0, translateY(-100%)) until
    # scrollY > 500 on desktop, matching the real landing page exactly -
    # without this the header is stuck in whatever scroll state the capture
    # happened to be taken at (visible if captured mid-scroll, permanently
    # hidden if captured at the very top), instead of actually reacting.
    "getElementById('mascot')",
    # Mobile hero header - some pages toggle it on scroll, others on a
    # click; either way it's the real per-page logic, not a substitute.
    "getElementById('header-mobile-home-hero')",
)

# The real production JS bundle isn't reusable in a static capture (it's an
# ES module importing build chunks the browser never saved, and/or requires
# a live Livewire backend). Bootstrap 5's own CSS already defines every state
# class these components need (.show, .active, .fade, .modal-backdrop, ...) -
# confirmed present in the captured stylesheet - so a small vanilla
# re-implementation of Bootstrap's data-api toggle contracts reproduces
# identical visual behavior for every standard component the prototype might
# use (navbar toggler, filter panels, modals, tabs), not just one page's
# specific widgets. This file is mockup scaffolding only - the real project
# already ships full Bootstrap JS, don't copy this file into it.
INTERACTIONS_JS = """// Local Bootstrap-5-compatible interaction layer for this mockup.
// Covers every standard data-bs-* component so prototypes "just work" without
// needing the production JS bundle (which isn't reusable from a static
// capture). Mockup scaffolding only - do not copy into the real project,
// which already has the full Bootstrap JS bundle.
(function () {
    function targetOf(trigger) {
        var sel = trigger.getAttribute('data-bs-target') || trigger.getAttribute('href');
        if (!sel || sel === '#') return null;
        try { return document.querySelector(sel); } catch (e) { return null; }
    }

    // --- Dropdown ---------------------------------------------------------
    function closeDropdowns(except) {
        document.querySelectorAll('.dropdown-menu.show').forEach(function (menu) {
            if (menu !== except) menu.classList.remove('show');
        });
        document.querySelectorAll('[data-bs-toggle="dropdown"].show').forEach(function (toggle) {
            if (toggle.parentElement.querySelector('.dropdown-menu') !== except) {
                toggle.classList.remove('show');
                toggle.setAttribute('aria-expanded', 'false');
            }
        });
    }

    function handleDropdown(toggle, event) {
        event.preventDefault();
        var menu = toggle.parentElement.querySelector('.dropdown-menu');
        var willOpen = menu && !menu.classList.contains('show');
        closeDropdowns();
        if (menu && willOpen) {
            menu.classList.add('show');
            toggle.classList.add('show');
            toggle.setAttribute('aria-expanded', 'true');
        }
    }

    // --- Collapse (navbar toggler, filter panels, accordions) --------------
    function handleCollapse(trigger, event) {
        event.preventDefault();
        var target = targetOf(trigger);
        if (!target) return;
        var isShown = target.classList.toggle('show');
        trigger.classList.toggle('collapsed', !isShown);
        trigger.setAttribute('aria-expanded', String(isShown));
        // Accordions: siblings in the same accordion collapse when one opens.
        var accordion = target.closest('.accordion');
        if (accordion && isShown) {
            accordion.querySelectorAll('.accordion-collapse.show').forEach(function (other) {
                if (other !== target) {
                    other.classList.remove('show');
                    var otherTrigger = accordion.querySelector('[data-bs-target="#' + other.id + '"]');
                    if (otherTrigger) {
                        otherTrigger.classList.add('collapsed');
                        otherTrigger.setAttribute('aria-expanded', 'false');
                    }
                }
            });
        }
    }

    // --- Modal / Offcanvas (share the same show/hide/backdrop shape) -------
    function showOverlay(el, kind) {
        el.classList.add('show');
        el.style.display = kind === 'modal' ? 'block' : '';
        el.setAttribute('aria-modal', 'true');
        el.removeAttribute('aria-hidden');
        document.body.classList.add(kind === 'modal' ? 'modal-open' : 'offcanvas-backdrop-open');
        var backdrop = document.createElement('div');
        backdrop.className = (kind === 'modal' ? 'modal-backdrop' : 'offcanvas-backdrop') + ' fade show';
        backdrop.dataset.mockupBackdropFor = el.id;
        document.body.appendChild(backdrop);
    }

    function hideOverlay(el, kind) {
        el.classList.remove('show');
        if (kind === 'modal') el.style.display = 'none';
        el.setAttribute('aria-hidden', 'true');
        el.removeAttribute('aria-modal');
        document.body.classList.remove(kind === 'modal' ? 'modal-open' : 'offcanvas-backdrop-open');
        document.querySelectorAll('[data-mockup-backdrop-for="' + el.id + '"]').forEach(function (b) { b.remove(); });
    }

    function overlayKindOf(el) {
        return el.classList.contains('offcanvas') ? 'offcanvas' : 'modal';
    }

    // --- Tabs / pills --------------------------------------------------------
    function handleTab(trigger, event) {
        event.preventDefault();
        var pane = targetOf(trigger);
        var navGroup = trigger.closest('.nav, .list-group');
        if (navGroup) {
            navGroup.querySelectorAll('.active').forEach(function (a) { a.classList.remove('active'); });
        }
        trigger.classList.add('active');
        trigger.setAttribute('aria-selected', 'true');
        if (pane) {
            var paneGroup = pane.closest('.tab-content');
            if (paneGroup) {
                paneGroup.querySelectorAll('.tab-pane.show.active').forEach(function (p) {
                    p.classList.remove('show', 'active');
                });
            }
            pane.classList.add('show', 'active');
        }
    }

    // --- Destructive actions (delete/hapus) --------------------------------
    // No backend to actually delete anything, but reusing the real app's own
    // delete-confirmation modal (same title/wording/buttons, already in the
    // capture) - then actually removing the row(s) on confirm - looks and
    // behaves like production instead of a generic browser confirm() popup.
    var pendingDeleteRow = null;

    function handleConfirm(trigger, event) {
        event.preventDefault();
        var message = trigger.getAttribute('data-mockup-confirm');
        if (!window.confirm(message)) return;
        var row = trigger.closest('tr, .card, li.list-group-item, .list-group-item');
        if (row) row.remove();
    }

    function handleBulkDelete(trigger, event) {
        event.preventDefault();
        var hasChecked = !!document.querySelector('tbody input[type="checkbox"]:checked');
        var targetSel = trigger.getAttribute(
            hasChecked ? 'data-mockup-bulk-delete-confirm' : 'data-mockup-bulk-delete-empty'
        );
        var modal = targetSel && document.querySelector(targetSel);
        if (modal) showOverlay(modal, 'modal');
    }

    function handleDeleteConfirmClick(trigger, event) {
        event.preventDefault();
        var kind = trigger.getAttribute('data-mockup-delete-confirm');
        var modal = trigger.closest('.modal');
        if (modal) hideOverlay(modal, 'modal');
        if (kind === 'row' && pendingDeleteRow) {
            pendingDeleteRow.remove();
        } else if (kind === 'bulk') {
            document.querySelectorAll('tbody input[type="checkbox"]:checked').forEach(function (cb) {
                var row = cb.closest('tr');
                if (row) row.remove();
            });
        }
        pendingDeleteRow = null;
    }

    document.addEventListener('click', function (event) {
        // Remember which row asked for the shared row-delete modal, before
        // the generic data-bs-toggle="modal" handling below opens it.
        var rowTrigger = event.target.closest('[data-mockup-delete-row-trigger]');
        if (rowTrigger) pendingDeleteRow = rowTrigger.closest('tr');

        var bulkTrigger = event.target.closest('[data-mockup-bulk-delete]');
        if (bulkTrigger) return handleBulkDelete(bulkTrigger, event);

        var deleteConfirm = event.target.closest('[data-mockup-delete-confirm]');
        if (deleteConfirm) return handleDeleteConfirmClick(deleteConfirm, event);

        var confirmTrigger = event.target.closest('[data-mockup-confirm]');
        if (confirmTrigger) return handleConfirm(confirmTrigger, event);

        var toggle = event.target.closest('[data-bs-toggle]');
        var dismiss = event.target.closest('[data-bs-dismiss]');

        if (toggle) {
            var kind = toggle.getAttribute('data-bs-toggle');
            if (kind === 'dropdown') return handleDropdown(toggle, event);
            if (kind === 'collapse') return handleCollapse(toggle, event);
            if (kind === 'tab' || kind === 'pill') return handleTab(toggle, event);
            if (kind === 'modal' || kind === 'offcanvas') {
                event.preventDefault();
                var el = targetOf(toggle);
                if (el) showOverlay(el, kind);
                return;
            }
        }

        if (dismiss) {
            var what = dismiss.getAttribute('data-bs-dismiss');
            if (what === 'alert') {
                event.preventDefault();
                var alertEl = dismiss.closest('.alert');
                if (alertEl) alertEl.remove();
                return;
            }
            if (what === 'modal' || what === 'offcanvas') {
                event.preventDefault();
                var overlay = dismiss.closest('.modal, .offcanvas');
                if (overlay) hideOverlay(overlay, overlayKindOf(overlay));
                return;
            }
        }

        // Backdrop click closes the modal/offcanvas it belongs to.
        if (event.target.dataset && event.target.dataset.mockupBackdropFor) {
            var owned = document.getElementById(event.target.dataset.mockupBackdropFor);
            if (owned) hideOverlay(owned, overlayKindOf(owned));
            return;
        }

        if (!event.target.closest('.dropdown-menu')) closeDropdowns();
    });

    // Flash-message alerts triggered by a real create/update request can't
    // fire in a static mockup (there's no backend) - but if the capture
    // included one already rendered (e.g. captured right after a save), its
    // dismiss button above already works. See manifest.md for a note on this.
})();

// A newer QUANTUM revision (seen in the maukuliah_* apps) uses its own plain
// `data-toggle`/`data-target`/`data-dismiss` contract (no `data-bs-` prefix)
// for dropdowns/modals/tabs/collapse, with different show-state classes
// (.dropdown__box.show, .modal.is-visible) than the Bootstrap 5 contract
// above - a separate, independent IIFE so neither layer can interfere with
// the other. Sidebar submenus and per-row modal content population on this
// revision are driven by real Alpine.js directives (x-data/x-show/x-on/
// $dispatch) instead of data-toggle, so those work via the restored Livewire
// bundle (which ships Alpine), not this file - see FUNCTIONAL_SCRIPTS.
(function () {
    function qnTargetOf(trigger) {
        var sel = trigger.getAttribute('data-target');
        if (!sel || sel === '#') return null;
        try { return document.querySelector(sel); } catch (e) { return null; }
    }

    // --- Dropdown (menu is a sibling within the same .dropdown wrapper,
    // never referenced by data-target) --------------------------------------
    function qnCloseDropdowns(except) {
        document.querySelectorAll('.dropdown__box.show, .dropdown__list.show').forEach(function (menu) {
            if (menu !== except) menu.classList.remove('show');
        });
        document.querySelectorAll('[data-toggle="dropdown"][aria-expanded="true"]').forEach(function (toggle) {
            var wrap = toggle.closest('.dropdown');
            var menu = wrap && wrap.querySelector('.dropdown__box, .dropdown__list');
            if (menu !== except) toggle.setAttribute('aria-expanded', 'false');
        });
    }

    function qnHandleDropdown(trigger, event) {
        event.preventDefault();
        var wrap = trigger.closest('.dropdown');
        var menu = wrap && wrap.querySelector('.dropdown__box, .dropdown__list');
        var willOpen = !!menu && !menu.classList.contains('show');
        qnCloseDropdowns();
        trigger.setAttribute('aria-expanded', String(willOpen));
        if (menu && willOpen) menu.classList.add('show');
    }

    // --- Collapse (e.g. sticky form-table toggler) --------------------------
    function qnHandleCollapse(trigger, event) {
        event.preventDefault();
        var target = qnTargetOf(trigger);
        if (!target) return;
        var isShown = target.classList.toggle('show');
        trigger.setAttribute('aria-expanded', String(isShown));
    }

    // --- Modal (the capture's own .modal__overlay/close icon already carry
    // data-dismiss="modal", so closing needs no synthetic backdrop) ---------
    function qnShowModal(modal) {
        modal.classList.add('on-opening');
        modal.removeAttribute('aria-hidden');
        modal.setAttribute('aria-modal', 'true');
        // Next frame so the opacity transition already defined in the
        // captured CSS (.modal.is-visible) actually plays, same as production.
        requestAnimationFrame(function () {
            modal.classList.remove('on-opening');
            modal.classList.add('is-visible');
        });
    }

    function qnHideModal(modal) {
        modal.classList.remove('is-visible');
        modal.classList.add('on-closing');
        modal.setAttribute('aria-hidden', 'true');
        modal.removeAttribute('aria-modal');
        setTimeout(function () { modal.classList.remove('on-closing'); }, 460);
    }

    // --- Tabs / pills --------------------------------------------------------
    function qnHandleTab(trigger, event) {
        event.preventDefault();
        var pane = qnTargetOf(trigger);
        var itemGroup = trigger.parentElement;
        if (itemGroup) {
            itemGroup.querySelectorAll(':scope > .active').forEach(function (a) {
                if (a !== trigger) a.classList.remove('active');
            });
        }
        trigger.classList.add('active');
        if (pane) {
            var paneGroup = pane.parentElement;
            if (paneGroup) {
                paneGroup.querySelectorAll(':scope > .active').forEach(function (p) {
                    if (p !== pane) p.classList.remove('active');
                });
            }
            pane.classList.add('active');
        }
    }

    document.addEventListener('click', function (event) {
        var toggle = event.target.closest('[data-toggle]');
        var dismiss = event.target.closest('[data-dismiss]');

        if (toggle) {
            var kind = toggle.getAttribute('data-toggle');
            if (kind === 'dropdown') return qnHandleDropdown(toggle, event);
            if (kind === 'collapse') return qnHandleCollapse(toggle, event);
            if (kind === 'tab' || kind === 'pill') return qnHandleTab(toggle, event);
            if (kind === 'modal') {
                event.preventDefault();
                var el = qnTargetOf(toggle);
                if (el) qnShowModal(el);
                return;
            }
        }

        if (dismiss && dismiss.getAttribute('data-dismiss') === 'modal') {
            event.preventDefault();
            var modal = dismiss.closest('.modal');
            if (modal) qnHideModal(modal);
            return;
        }

        if (!event.target.closest('.dropdown')) qnCloseDropdowns();
    });

    document.addEventListener('keydown', function (event) {
        if (event.key !== 'Escape') return;
        qnCloseDropdowns();
        document.querySelectorAll('.modal.is-visible, .modal.on-opening').forEach(qnHideModal);
    });
})();

// Selectize (jQuery plugin) turns a plain <select class="selectized"> into a
// searchable multi-select box - the capture always has the real, hidden
// <select> (style="display:none"), but the actual call that upgrades it into
// the widget lives in a production JS chunk this tool can't recover (same
// "ES module chunk the browser never saved" limitation as everywhere else in
// this file) - so it's re-issued here, once, using the real vendored
// Selectize/jQuery (see FUNCTIONAL_SCRIPTS), not a hand-rolled substitute.
// A no-op on every page that doesn't have both libraries loaded.
(function () {
    if (typeof window.jQuery === 'undefined' || typeof window.jQuery.fn === 'undefined'
        || typeof window.jQuery.fn.selectize === 'undefined') return;
    window.jQuery('select.selectized').each(function () {
        if (this.selectize) return;
        window.jQuery(this).selectize();
    });
})();

// Form input helpers from the production core.js (not recoverable from the
// capture): the password show/hide eye and the clear-input "x". Their icons
// are pure CSS ([data-visibility]/[data-clear]); only the click behaviour is
// missing without this.
document.addEventListener('click', function (e) {
    var t = e.target;
    if (!t || !t.matches) return;
    if (t.matches("[data-clear='input']")) {
        var inp = t.parentNode && t.parentNode.querySelector('.form-control__input');
        if (inp) {
            inp.value = '';
            inp.dispatchEvent(new Event('change'));
            inp.dispatchEvent(new Event('input', { bubbles: true }));
        }
    }
    if (t.matches("[data-visibility='input']")) {
        var field = t.parentNode && t.parentNode.querySelector('input');
        if (field) {
            var show = t.dataset.type !== 'text';
            field.type = show ? 'text' : 'password';
            t.dataset.type = show ? 'text' : 'password';
        }
    }
});

// Preference form helpers (mockup scaffolding - the real app does this with
// Livewire/Alpine): live filter for long option lists,
// price-range presets that fill the min/max inputs, and Rupiah formatting.
(function () {
    function fmt(digits) {
        return digits ? 'Rp ' + digits.replace(/\B(?=(\d{3})+(?!\d))/g, '.') : '';
    }
    document.addEventListener('input', function (e) {
        var t = e.target;
        if (t.matches && t.matches('[data-filter-list]')) {
            var list = document.querySelector(t.getAttribute('data-filter-list'));
            if (!list) return;
            var q = t.value.trim().toLowerCase(), shown = 0;
            list.querySelectorAll('.option-card').forEach(function (c) {
                var hit = !q || c.textContent.toLowerCase().indexOf(q) !== -1;
                c.hidden = !hit;
                if (hit) shown++;
            });
            list.querySelectorAll('.option-group').forEach(function (g) {
                g.hidden = !g.querySelector('.option-card:not([hidden])');
            });
            var empty = document.querySelector('[data-filter-empty="' + t.getAttribute('data-filter-list') + '"]');
            if (empty) empty.hidden = shown > 0;
        }
        if (t.matches && t.matches('[data-money]')) {
            t.value = fmt(t.value.replace(/\D/g, ''));
            document.querySelectorAll('[data-range-preset]').forEach(function (r) { r.checked = false; });
        }
    });
    document.addEventListener('change', function (e) {
        var t = e.target;
        if (t.matches && t.matches('[data-range-preset]')) {
            var min = document.getElementById('input__price-min');
            var max = document.getElementById('input__price-max');
            if (min) min.value = fmt(t.getAttribute('data-min'));
            if (max) max.value = fmt(t.getAttribute('data-max'));
        }
    });
})();
"""

CSS_URL_RE = re.compile(r"url\(\s*(['\"]?)(?!data:)([^'\")]+)\1\s*\)")


def find_known_local_asset(basename):
    for prefix, suffix, path in KNOWN_LOCAL_ASSETS:
        if basename.startswith(prefix) and basename.endswith(suffix) and path.exists():
            return path
    return None


def localize_css_urls(css_text, out_dir, css_dir=None):
    """Resolve every url() in a CSS blob to something local: a known
    first-party QUANTUM asset if we have one, otherwise `none` - never left
    pointing at an external domain."""
    stats = Counter()
    vendor_dir = out_dir / "_assets" / "vendor" / "local-assets"
    images_dir = out_dir / "_assets" / "vendor" / "images"
    # url()s are resolved by the browser relative to the CSS FILE, not the page:
    # a stylesheet in _assets/captured/ needs '../vendor/...', while an inline
    # <style> in the page needs '_assets/vendor/...'.
    css_dir = css_dir or out_dir

    def _sub(m):
        raw_url = m.group(2)
        basename = raw_url.split("#")[0].split("?")[0].split("/")[-1]
        local_src = find_known_local_asset(basename)
        if local_src:
            dest = vendor_dir / basename
            if not dest.exists():
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(local_src, dest)
            stats["local_assets_matched"] += 1
            return f"url({Path(os.path.relpath(dest, css_dir)).as_posix()})"
        # Relative refs into QUANTUM's image tree ('./../../assets/images/icons/
        # input-email.svg', patterns, heroicons...) - these are the form-input
        # icons, password-visibility toggles, chevrons and card patterns. The
        # capture never saves them, but QUANTUM ships the originals.
        marker = "assets/images/"
        clean = raw_url.split("#")[0].split("?")[0]
        if marker in clean and not clean.startswith(("http://", "https://")):
            rel = clean.split(marker, 1)[1]
            img_src = QUANTUM_ASSET_ROOT / "assets" / "images" / rel
            if img_src.exists():
                dest = images_dir / rel
                if not dest.exists():
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(img_src, dest)
                stats["local_assets_matched"] += 1
                return f"url({Path(os.path.relpath(dest, css_dir)).as_posix()})"
            stats["image_assets_missing"] += 1
            return "none"
        if raw_url.startswith("http://") or raw_url.startswith("https://") or raw_url.startswith("/"):
            stats["external_urls_dropped"] += 1
            return "none"
        return m.group(0)  # same-directory relative ref - leave alone, harmless if missing

    return CSS_URL_RE.sub(_sub, css_text), stats


# Chrome/Edge stamp 'saved from url=(NNN)https://host/path' as the first HTML
# comment in a 'Webpage, Complete' capture - this is the only record of which
# real app route a given mockup corresponds to, which is what makes
# cross-page navigation (navbar, "Tambah", row actions -> the right mockup)
# possible instead of dead-ending every internal link at '#'.
CAPTURE_URL_RE = re.compile(r"saved from url=\(\d+\)(https?://[^\s\"'<>]+)")
ID_SEGMENT_RE = re.compile(
    r"^\d+$|^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)
# Some apps key records by numeric/UUID id (matched above); others key them by
# a human slug instead - 'beasiswa-prestasi-akademik-unggulan-2026',
# '20242025-ganjil', 'biaya-tambahan-123'. A bare hyphen isn't a safe signal
# on its own (this app also has plenty of *static* hyphenated route segments:
# 'admission-cycles', 'school-profilings', 'university-majors' etc.) - but
# checked against every path this tool has actually seen captured, every
# segment containing a digit is a per-record slug/id, never a fixed route
# keyword, so that's the additional, safe-for-this-corpus signal.


def extract_capture_path(raw_html_text):
    """Pull the path (no domain, no query string) this capture was saved
    from, e.g. '/v2/kerjasama/45'. None if the capture has no such comment
    (e.g. hand-built, or saved via 'Copy outerHTML' which drops it)."""
    m = CAPTURE_URL_RE.search(raw_html_text)
    if not m:
        return None
    return urlparse(m.group(1)).path or "/"


def extract_capture_domain(raw_html_text):
    """The host this capture was saved from, e.g. 'maukuliah.id' - used to
    scrub bare mentions of the live domain out of visible TEXT content (a
    "copy this landing page URL" table cell, an embed-code example), not
    just attributes. None if there's no 'saved from url=' comment."""
    m = CAPTURE_URL_RE.search(raw_html_text)
    if not m:
        return None
    return urlparse(m.group(1)).netloc or None


# A record slug with zero digits ('universitas-sentra-vidya-utama',
# 'pariwisata-dan-perhotelan') can't be told apart from a static route
# keyword ('admission-cycles', 'school-profilings') by shape alone - both are
# just hyphenated words. What DOES distinguish them: a slug like this only
# ever shows up as a direct child of a collection whose *own* list page is
# itself a captured route ('.../master/universities' exists on its own,
# '.../universities/{slug}' is one level under it). So instead of guessing
# from the string, ask the corpus of raw captures directly - if the parent
# path is a route we've actually captured, the segment under it is a record
# slug, not a fixed keyword. 'create'/'edit' are excluded even though they
# sit in that same slot, so they stay their own distinct literal pattern
# instead of colliding with a sibling record's detail page.
STATIC_ACTION_SEGMENTS = {"create", "edit"}
_known_capture_paths_cache = None


def known_capture_paths():
    """Every '.../saved from url=' path across ALL raw captures on disk
    (not just the one file.path_pattern happens to be called for right now),
    so recognizing '.../{collection}/{slug}' doesn't depend on what order
    pages happen to get built in - see path_pattern."""
    global _known_capture_paths_cache
    if _known_capture_paths_cache is not None:
        return _known_capture_paths_cache
    paths = set()
    raw_dir = MOCKUPS / "raw"
    if raw_dir.exists():
        for html_path in raw_dir.rglob("*.html"):
            text = html_path.read_text(encoding="utf-8", errors="ignore")
            p = extract_capture_path(text)
            if p:
                paths.add(p)
    _known_capture_paths_cache = paths
    return paths


def path_pattern(path):
    """Normalize a path so different records of the same route (different
    ids/slugs) match: '/v2/kerjasama/45' and '/v2/kerjasama/78' both become
    '/v2/kerjasama/{id}' - and so do 'scholarships/beasiswa-a-2026/edit' and
    'scholarships/beasiswa-b-2027/edit' (digit-bearing slug, see
    ID_SEGMENT_RE), AND 'universities/universitas-a' and 'universities/
    universitas-b' (no digit, but both sit directly under the captured
    '.../universities' list route - see known_capture_paths)."""
    segments = path.split("/")

    def is_id(i):
        seg = segments[i]
        if seg in STATIC_ACTION_SEGMENTS:
            return False
        if ID_SEGMENT_RE.match(seg) or any(c.isdigit() for c in seg):
            return True
        parent = "/".join(segments[:i])
        return parent in known_capture_paths()

    return "/".join("{id}" if is_id(i) else segments[i] for i in range(len(segments)))


def load_route_map():
    if ROUTE_MAP_PATH.exists():
        return load_json(ROUTE_MAP_PATH)
    return {}


def save_route_map(route_map):
    ROUTE_MAP_PATH.parent.mkdir(parents=True, exist_ok=True)
    ROUTE_MAP_PATH.write_text(
        json.dumps(route_map, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")


def _pick_canonical(candidates, self_id=None):
    """Same route, several captures (e.g. a detail page captured plain, and
    again right after a create/edit shows a flash banner on that same URL).
    Preference order: (1) the page currently being linked FROM, if its own
    route matches - a nav tab/breadcrumb pointing at "itself" should stay on
    itself, not jump to a sibling capture of the same URL; (2) the
    plain/canonical capture, so "Detail" from a list doesn't land on a
    fleeting "berhasil diubah" state; (3) a *-success capture only as a last
    resort, if it's the only mockup that route has."""
    if not candidates:
        return None
    if self_id in candidates:
        return self_id
    preferred = [c for c in candidates if "success" not in c]
    return (preferred or candidates)[0]


def resolve_route(path, route_map, self_id=None):
    """Exact path match wins; otherwise fall back to pattern match (handles
    '/kerjasama/45' finding a mockup captured from '/kerjasama/78'). Returns
    the matching page_id ('module/page'), or None."""
    if not path:
        return None
    pattern = path_pattern(path)
    exact_matches, pattern_matches = [], []
    for pid, info in route_map.items():
        if info.get("path") == path:
            exact_matches.append(pid)
        elif info.get("pattern") == pattern:
            pattern_matches.append(pid)
    return (_pick_canonical(exact_matches, self_id)
            or _pick_canonical(pattern_matches, self_id))


NOISE_CLASS_PREFIXES = ("sf-dump", "sf-toolbar", "phpdebugbar", "plasmo-csui")
NOISE_CLASS_TOKENS = {"sf-js-enabled"}
NOISE_TAGS = ("plasmo-csui",)
# <plasmo-csui> (a browser-extension injection) wraps a <template
# shadowrootmode="open"> that libxml2's HTML parser doesn't understand -
# it's not just noise to decompose *after* parsing, it corrupts the parser's
# insertion-mode state badly enough that the real <body>'s own attributes
# (x-data, class, ...) get silently dropped by the time BeautifulSoup sees
# them. Cut it out of the raw text before parsing at all, rather than after.
PRE_PARSE_STRIP_RE = re.compile(r"<plasmo-csui\b.*?</plasmo-csui>", re.S)
# lxml's HTML parser silently DROPS `@event="..."` attributes entirely (Vue/
# Alpine's shorthand for `x-on:event="..."`) - confirmed: BeautifulSoup(html,
# 'lxml') on a tag with `@click="..."` comes out with no click handler at all,
# while the equivalent `x-on:click="..."` survives untouched. Since `@` isn't
# a valid XML/HTML attribute-name start character, libxml2 seems to just
# discard it rather than erroring - so every `@click`/`@click.away`/etc.
# needs rewriting to its `x-on:` spelling (functionally identical to Alpine)
# in the raw text BEFORE parsing, not after (by then it's already gone).
# Lookbehind requires a preceding whitespace so this only matches inside a
# tag's attribute list, never e.g. an email address in body text.
ALPINE_AT_SHORTHAND_RE = re.compile(r"(?<=[\s])@([a-zA-Z][\w:.-]*)=(?=[\"'])")
# Framework-glue attributes with no meaning in a static mockup - Laravel
# Turbo/Turbolinks navigation hints, Livewire wiring, CSRF plumbing. Stripped
# so the markup a developer copies back into the real project isn't cluttered
# with attributes that only make sense wired to a live backend.
NOISE_ATTR_PREFIXES = ("data-turbo", "data-navigate-track")
NOISE_ATTR_NAMES = {"data-csrf", "data-update-uri", "data-turbolinks-eval"}
# Inline <style> blocks with no matching elements left after cleanup (debug
# toolbar CSS, browser-extension overlay CSS) - dropped by content signature.
NOISE_STYLE_SIGNATURES = ("phpdebugbar", "sf-dump", "plasmo", "give-freely", "gf-app")
# First hyphen-segment (or whole class, for bare words) of known Bootstrap-family
# utility/component classes. Covers responsive infixes like `pb-md-0`, `gap-lg-3`.
BOOTSTRAP_UTILITY_PREFIXES = {
    "d", "col", "row", "g", "gx", "gy", "text", "bg", "btn", "nav", "dropdown",
    "badge", "align", "justify", "gap", "rounded", "border", "shadow", "fs", "fw",
    "w", "h", "flex", "sticky", "container", "p", "pt", "pb", "ps", "pe", "px", "py",
    "m", "mt", "mb", "ms", "me", "mx", "my", "vr", "small", "link", "card", "modal",
    "breadcrumb", "fade", "active", "img", "object", "z", "opacity", "overflow",
    "position", "top", "start", "end", "bottom", "ratio", "order", "float",
    "clearfix", "visually", "list", "table", "form", "input", "collapse", "offcanvas",
    "tab", "toast", "spinner", "pagination", "progress", "tooltip", "popover",
    "navbar", "lh", "align-items", "justify-content",
}
HEX_COLOR_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")


def slugify(name):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", name).strip("-").lower()
    return s or "page"


def parse_target(raw_path, arg=None):
    """'kerjasama/daftar' -> ('kerjasama', 'daftar'); 'dashboard' -> ('dashboard',
    'index'); no arg -> module from the raw filename, page 'index'."""
    parts = [p for p in (arg or raw_path.stem).replace("\\", "/").split("/") if p]
    if len(parts) == 1:
        return slugify(parts[0]), "index"
    return slugify(parts[0]), slugify("-".join(parts[1:]))


def page_id(module, page):
    return f"{module}/{page}"


API_VERSION_SEGMENTS = {"v1", "v2", "v3", "api"}


def suggest_module(capture_path):
    """The real app groups pages by URL, not by what a human decides to call
    them - '/v2/kerjasama/dashboard' belongs to the *kerjasama* module even
    though the page itself is a "dashboard". Used only to sanity-check the
    module the build was actually asked to use (never overrides it), so a
    page doesn't accidentally end up isolated in its own module folder
    just because of what it happened to be named."""
    if not capture_path:
        return None
    segments = [s for s in capture_path.split("/") if s]
    while segments and segments[0].lower() in API_VERSION_SEGMENTS:
        segments = segments[1:]
    return slugify(segments[0]) if segments else None


def relative_link(current_module, target_module, target_page):
    """href from the page being written to the target page's .html file -
    same-module links stay a bare filename (sibling in the same folder),
    cross-module links go up one level into the other module's folder."""
    filename = f"{target_page}.html"
    return filename if target_module == current_module else f"../{target_module}/{filename}"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def find_capture_assets_dir(raw_html_path):
    """Browser 'Save Complete' saves a sibling '<name>_files' folder."""
    candidate = raw_html_path.parent / f"{raw_html_path.stem}_files"
    if candidate.exists():
        return candidate
    # Several pages of one flow can share a single asset folder: '_files'
    # next to the HTML files (e.g. raw/maukuliah_preferensi/_files).
    shared = raw_html_path.parent / "_files"
    return shared if shared.exists() else None


# The real app already ships a "Hapus X? Data tidak dapat dikembalikan"
# confirmation modal in the markup - reuse THAT verbatim (title, wording,
# button labels, animation) instead of a generic browser confirm(), so the
# delete flow looks and feels identical to production.
DELETE_MODAL_TITLE_RE = re.compile(r"hapus", re.I)
DELETE_MODAL_BODY_RE = re.compile(r"yakin|dikembalikan", re.I)
BULK_MODAL_ID_HINTS = ("many", "checked", "bulk", "all")
NO_SELECTION_TITLE_RE = re.compile(r"pilih.*terlebih dahulu|centang.*terlebih dahulu", re.I)


def find_confirm_button(modal):
    """The footer button that actually performs the delete - i.e. not the
    Cancel/close one (those carry data-bs-dismiss)."""
    footer = modal.find(class_="modal-footer")
    if not footer:
        return None
    for btn in footer.find_all(["button", "a"]):
        if not btn.has_attr("data-bs-dismiss"):
            return btn
    return None


def classify_delete_modals(soup):
    """Find, among all modals already in the capture: the per-row delete
    confirmation, the bulk (checked-rows) delete confirmation, and the
    "you didn't select anything" warning - by title/body wording rather than
    hardcoded ids, so this works on any page using the same QUANTUM pattern,
    not just this one."""
    row_modal = bulk_modal = empty_modal = None
    for modal in soup.find_all("div"):
        classes = modal.get("class") or []
        if "modal" not in classes:
            continue
        title_el = modal.find(class_="modal-title")
        body_el = modal.find(class_="modal-body")
        title = title_el.get_text(strip=True).lower() if title_el else ""
        body = body_el.get_text(strip=True).lower() if body_el else ""
        modal_id = (modal.get("id") or "").lower()
        if DELETE_MODAL_TITLE_RE.search(title) and DELETE_MODAL_BODY_RE.search(body):
            if any(hint in modal_id for hint in BULK_MODAL_ID_HINTS) and "row" not in modal_id:
                bulk_modal = bulk_modal or modal
            else:
                row_modal = row_modal or modal
        elif NO_SELECTION_TITLE_RE.search(title):
            empty_modal = empty_modal or modal
    return row_modal, bulk_modal, empty_modal


def wire_delete_modals(soup):
    """Point every trash-icon trigger at the real delete-confirmation modal
    already in the capture (row-level or bulk), and tag that modal's actual
    "Hapus" button so mockup-interactions.js knows to remove the row(s) and
    close the modal when it's clicked. Falls back to a plain confirm() only
    for a trigger with no matching modal in the document at all."""
    stats = Counter()
    row_modal, bulk_modal, empty_modal = classify_delete_modals(soup)

    if row_modal is not None:
        btn = find_confirm_button(row_modal)
        if btn is not None:
            btn["data-mockup-delete-confirm"] = "row"
    if bulk_modal is not None:
        btn = find_confirm_button(bulk_modal)
        if btn is not None:
            btn["data-mockup-delete-confirm"] = "bulk"

    for icon in soup.find_all(class_=lambda c: c and "trash" in c):
        trigger = icon.find_parent(["a", "button"])
        if not trigger or trigger.has_attr("data-mockup-confirm") or trigger.has_attr("data-bs-toggle"):
            continue
        row = trigger.find_parent("tr")
        if row is not None and row_modal is not None:
            trigger["data-bs-toggle"] = "modal"
            trigger["data-bs-target"] = f"#{row_modal['id']}"
            trigger["data-mockup-delete-row-trigger"] = "1"
            stats["destructive_confirms_wired"] += 1
        elif row is None and (bulk_modal is not None or empty_modal is not None):
            trigger["data-mockup-bulk-delete"] = "1"
            if bulk_modal is not None:
                trigger["data-mockup-bulk-delete-confirm"] = f"#{bulk_modal['id']}"
            if empty_modal is not None:
                trigger["data-mockup-bulk-delete-empty"] = f"#{empty_modal['id']}"
            stats["destructive_confirms_wired"] += 1
        else:
            trigger["data-mockup-confirm"] = "Yakin ingin menghapus data ini? (mockup - tidak tersambung ke server)"
            stats["destructive_confirms_wired"] += 1

    return stats


def strip_noise(soup):
    stats = Counter()
    kept_inline_scripts = []

    for tag in soup.find_all("script", src=False):
        content = tag.string or tag.get_text() or ""
        if any(sig in content for sig in FUNCTIONAL_INLINE_SCRIPT_SIGNATURES):
            kept_inline_scripts.append(content)
            stats["functional_inline_scripts_kept"] += 1
        else:
            stats["script_tags_removed"] += 1
        tag.decompose()

    for tag in soup.find_all(NOISE_TAGS):
        tag.decompose()
        stats["extension_tags_removed"] += 1

    for tag in soup.find_all(True):
        if tag.attrs is None:
            continue  # already removed as a child of a decomposed ancestor
        classes = tag.get("class") or []
        tag_id = tag.get("id") or ""
        if any(c.startswith(NOISE_CLASS_PREFIXES) for c in classes) or tag_id.startswith(NOISE_CLASS_PREFIXES):
            tag.decompose()
            stats["debug_toolbar_blocks_removed"] += 1

    for tag in soup.find_all(True):
        if tag.attrs is None:
            continue
        # Livewire 3's confirm-before-destructive-action API - the attribute
        # value IS the confirmation message. Capture it before stripping so a
        # delete/destroy button still asks before "deleting" (removing the
        # row locally) instead of silently doing nothing.
        if tag.has_attr("wire:confirm") and not tag.has_attr("data-mockup-confirm"):
            tag["data-mockup-confirm"] = tag["wire:confirm"]
            stats["destructive_confirms_wired"] += 1
        # wire: directives need a live Livewire component root to do anything
        # (real requests never work in a static capture anyway) - but x-data/
        # x-init are pure client-side Alpine state with no backend involved,
        # and when the capture's own Livewire bundle is restored (it ships
        # Alpine - see FUNCTIONAL_SCRIPTS), stripping them would remove the
        # very scope x-on:click/x-show/$dispatch elsewhere on the same
        # element tree depend on, breaking Alpine-driven dropdowns/submenus/
        # modal population for no reason. Only wire:* is noise here.
        wire_attrs = [a for a in tag.attrs if a.startswith("wire:")]
        for a in wire_attrs:
            del tag[a]
            stats["livewire_alpine_attrs_removed"] += 1
        # A script tag's own data-* attrs are its boot config (e.g. Livewire
        # reads data-csrf/data-update-uri off itself), not backend wiring on
        # a content element - only strip these from tags that AREN'T one of
        # the scripts we're about to restore (see restore_functional_scripts).
        is_restored_script = tag.name == "script" and tag.get("src", "").split("/")[-1] in (
            raw for raw, _clean in FUNCTIONAL_SCRIPTS
        )
        noise_attrs = [] if is_restored_script else [
            a for a in tag.attrs if a.startswith(NOISE_ATTR_PREFIXES) or a in NOISE_ATTR_NAMES
        ]
        for a in noise_attrs:
            del tag[a]
            stats["framework_glue_attrs_removed"] += 1

    stats.update(wire_delete_modals(soup))

    for tag in soup.find_all("canvas"):
        if tag.has_attr("style"):
            del tag["style"]  # Chart.js recomputes this on init - stale capture-time values otherwise
            stats["chart_canvas_styles_cleared"] += 1

    for tag in soup.find_all("link", rel=lambda r: r in ("preload", "modulepreload", "dns-prefetch", "preconnect")):
        tag.decompose()
        stats["preload_links_removed"] += 1

    for tag in soup.find_all("style"):
        text = (tag.string or "").lower()
        if any(sig in text for sig in NOISE_STYLE_SIGNATURES):
            tag.decompose()
            stats["noise_style_blocks_removed"] += 1

    if soup.title and soup.title.string:
        soup.title.string.replace_with(soup.title.get_text(strip=True))

    for comment in soup.find_all(string=lambda t: isinstance(t, Comment)):
        comment.extract()
        stats["comments_removed"] += 1

    return stats, kept_inline_scripts


def vendor_quantum_css(out_dir):
    """Copy the QUANTUM CSS bundle *and* every font/icon it references into
    out_dir/_assets/vendor, rewriting url()s to match. Regenerated on every
    run (but skipped once already present - shared by every page in this
    module), so it stays synced with QUANTUM - but unlike a bare
    cross-directory <link>, it also works when the mockup is opened from a
    sandboxed webview or a dev server rooted at (or below) the mockup's own
    folder, since nothing needs to be reached by climbing back out to
    QUANTUM/ at view-time.
    """
    stats = Counter()
    if not QUANTUM_LIVE_CSS.exists():
        return None, stats

    out_css = out_dir / "_assets" / "quantum.css"
    if out_css.exists():
        return "_assets/quantum.css", stats  # already vendored for this module

    text = QUANTUM_LIVE_CSS.read_text(encoding="utf-8", errors="ignore")
    vendor_dir = out_dir / "_assets" / "vendor"
    replacements = {}

    for m in CSS_URL_RE.finditer(text):
        full_match, raw_url = m.group(0), m.group(2)
        if full_match in replacements:
            continue
        clean_url = raw_url.split("#")[0].split("?")[0]
        if clean_url.startswith("/"):
            src = QUANTUM_ASSET_ROOT / clean_url.lstrip("/")
            mirror_rel = Path(clean_url.lstrip("/"))
        else:
            src = (QUANTUM_LIVE_CSS.parent / clean_url).resolve()
            try:
                mirror_rel = src.relative_to(QUANTUM_ASSET_ROOT.resolve())
            except ValueError:
                mirror_rel = Path("external") / src.name
        if not src.exists():
            stats["assets_not_found"] += 1
            continue
        dest = vendor_dir / mirror_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
        stats["assets_copied"] += 1
        replacements[full_match] = f"url({Path(os.path.relpath(dest, out_dir)).as_posix()})"

    for old, new in replacements.items():
        text = text.replace(old, new)

    out_css.write_text(text, encoding="utf-8")
    return "_assets/quantum.css", stats


def vendor_captured_stylesheets(soup, out_dir, capture_assets_dir):
    """The browser capture's own CSS is the ground truth for how the page
    actually looked in production - always prefer it over the (possibly
    stale) local QUANTUM checkout when it's available. Collect the original
    <link rel=stylesheet> hrefs before they're dropped, copy any that exist
    in the capture's asset folder into out_dir/_assets/captured/ (shared by
    every page in this module - skipped if another page already vendored the
    identical filename, which is the normal case since it's the same app
    CSS bundle for every page), and return the new hrefs in original order
    (dedup by filename - captures sometimes repeat a link, e.g. from a
    client-side navigation re-render)."""
    stats = Counter()
    seen, ordered_filenames = set(), []
    for tag in soup.find_all("link", rel="stylesheet"):
        fname = tag.get("href", "").split("/")[-1]
        if fname and fname not in seen:
            seen.add(fname)
            ordered_filenames.append(fname)
        tag.decompose()
        stats["captured_stylesheets_dropped"] += 1

    hrefs = []
    if capture_assets_dir is not None:
        dest_dir = out_dir / "_assets" / "captured"
        for fname in ordered_filenames:
            src = capture_assets_dir / fname
            if not src.exists():
                continue
            # Some captures save a stylesheet at an extensionless URL (e.g. a
            # dynamic route) - force a .css name so file:// MIME sniffing
            # still treats it as a stylesheet.
            out_name = fname if fname.lower().endswith(".css") else f"{fname}.css"
            dest = dest_dir / out_name
            href = f"_assets/captured/{out_name}"
            if dest.exists():
                hrefs.append(href)  # already vendored by an earlier page in this module
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            text = src.read_text(encoding="utf-8", errors="ignore")
            text, url_stats = localize_css_urls(text, out_dir, css_dir=dest.parent)
            stats.update(url_stats)
            dest.write_text(text, encoding="utf-8")
            hrefs.append(href)
            stats["captured_stylesheets_vendored"] += 1

    return hrefs, stats


def ensure_head(soup):
    head = soup.head
    if head is None:
        # Some captures have no explicit <head> (lxml won't synthesize one)
        # - create one and place it first, browsers tolerate this.
        head = soup.new_tag("head")
        if soup.html:
            soup.html.insert(0, head)
        else:
            soup.insert(0, head)
    return head


def restore_functional_scripts(soup, out_dir, capture_assets_dir, kept_inline_scripts, extra_modulepreload_names=()):
    """Drop every captured <script src> except the Chart.js stack (verified
    self-contained, no further imports) - copy those locally under a clean
    name into out_dir/_assets (shared across the module's pages, copied once),
    keep the tag, and re-append the chart-init inline script (with its real
    data, always page-specific) plus our own interaction layer at the end of
    body. extra_modulepreload_names covers scripts the page genuinely loads
    but never as a literal <script src=...> - a Vite entry point can import a
    chunk only via <link rel=modulepreload>, then execute it through its own
    module graph rather than a second static tag - see find_modulepreload_
    functional_scripts, called before strip_noise removes those hints."""
    stats = Counter()
    js_dir = out_dir / "_assets"

    def vendor_script(fname, match):
        dest = js_dir / match
        if not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(capture_assets_dir / fname, dest)
        stats["functional_scripts_vendored"] += 1

    kept_names = []
    kept_attrs = {}
    for tag in soup.find_all("script", src=True):
        fname = tag["src"].split("/")[-1]
        match = next((clean for raw, clean in FUNCTIONAL_SCRIPTS if raw == fname), None)
        if match and capture_assets_dir is not None and (capture_assets_dir / fname).exists():
            if match not in kept_names:
                vendor_script(fname, match)
                kept_names.append(match)
                # Preserve data-* attrs from the original tag (e.g. Livewire's
                # data-csrf/data-update-uri) - restoring the script alone
                # isn't enough if the library reads its own boot config off
                # its own <script> tag.
                kept_attrs[match] = {k: v for k, v in tag.attrs.items() if k.startswith("data-")}
        tag.decompose()
        stats["captured_scripts_dropped"] += 1

    if capture_assets_dir is not None:
        for fname, match in extra_modulepreload_names:
            if match in kept_names or not (capture_assets_dir / fname).exists():
                continue
            vendor_script(fname, match)
            kept_names.append(match)

    body = soup.body
    if body is None:
        return stats
    if "livewire.min.js" in kept_names:
        stats["livewire_restored"] = True
    for name in kept_names:
        new_tag = soup.new_tag("script", src=f"_assets/{name}")
        for k, v in kept_attrs.get(name, {}).items():
            new_tag[k] = v
        body.append(new_tag)
    for content in kept_inline_scripts:
        tag = soup.new_tag("script")
        tag.string = content
        body.append(tag)

    interactions_path = js_dir / "mockup-interactions.js"
    if not interactions_path.exists():
        interactions_path.parent.mkdir(parents=True, exist_ok=True)
        interactions_path.write_text(INTERACTIONS_JS, encoding="utf-8")
    body.append(soup.new_tag("script", src="_assets/mockup-interactions.js"))
    stats["functional_scripts_vendored"] += 1 if kept_inline_scripts else 0

    return stats


def localize_inline_styles(soup, out_dir):
    """Same treatment as vendored CSS files, but for <style> blocks left
    inline in <head> (e.g. the .qn-header-pattern/.qn-sidebar background
    images) - resolve to a local QUANTUM asset or drop to `none`."""
    stats = Counter()
    for tag in soup.find_all("style"):
        text = tag.string or tag.get_text() or ""
        if "url(" not in text:
            continue
        new_text, url_stats = localize_css_urls(text, out_dir)
        stats.update(url_stats)
        if new_text != text:
            tag.string = new_text
    return stats


# Pages of the authentication flow and where a completed login/register
# continues (post-auth landing page of the user area).
AUTH_PAGES = {"login/index", "register/index"}
AUTH_LAYOUT_CSS = (
    # Kolom ilustrasi kanan setinggi layar dan menempel saat scroll, sama dengan
    # halaman preferensi, supaya ukurannya tidak berubah mengikuti tinggi form.
    ".main_advanced-login{min-height:100vh}"
    ".main_advanced-login .advanced-login__wrapper{position:sticky;top:0;"
    "align-self:flex-start;box-sizing:border-box;height:100vh}"
)
AUTH_NEXT = "preferences/index"  # post-auth: optional preference pipeline, which then continues to user/index


def resolve_internal_links(soup, module, page, route_map):
    """Every <a href>/<form action> pointing at an external http(s) origin
    (navbar tabs, "Tambah"/Edit/Detail buttons, logout, etc.) either becomes
    a real link to a sibling mockup (if one's been built for that route) or
    gets neutralized to '#' with the original path kept on
    data-mockup-unresolved so relink_existing_mockups() can wire it up the
    moment a matching mockup does get built - that's what makes this dynamic
    instead of a one-shot dead end."""
    stats = Counter()
    pending_paths = set()
    self_id = page_id(module, page)

    def handle(tag, attr):
        url = tag[attr]
        if not (url.startswith("http://") or url.startswith("https://")):
            return
        path = urlparse(url).path or "/"
        target = resolve_route(path, route_map, self_id=self_id)
        if not target and path.rstrip("/").endswith("/login-as") and "crm/dashboard" in route_map:
            # Super-admin's "Login Sebagai Kampus" impersonates that
            # institution and drops you into ITS crm panel - there's no
            # standalone "login-as" page to capture (it's a redirect, not a
            # view), so the truest mockup equivalent is the crm dashboard
            # itself, not a dead '#'.
            target = "crm/dashboard"
        # Auth flow: a successful login/register (form POST, or the Google
        # OAuth button) lands on the user area in production, so the static
        # mockup continues there instead of reloading the auth page itself.
        if (tag.name == "form" and target in AUTH_PAGES) or path.rstrip("/") == "/auth/google":
            if AUTH_NEXT in route_map:
                target = AUTH_NEXT
            elif "user/index" in route_map:
                target = "user/index"
        if target:
            target_module, target_page = target.split("/", 1)
            tag[attr] = relative_link(module, target_module, target_page)
            stats["internal_links_resolved"] += 1
        else:
            tag[attr] = "#"
            tag["data-mockup-unresolved"] = path
            stats["internal_links_pending"] += 1
            pending_paths.add(path)

    for tag in soup.find_all("a", href=True):
        handle(tag, "href")
    for tag in soup.find_all("form", action=True):
        handle(tag, "action")
    return stats, sorted(pending_paths)


# Last-resort safety net, NOT a substitute for the targeted handling above -
# a real network request to a live/testing backend from a "static, offline"
# mockup is a data-safety incident waiting to happen (e.g. a delete
# confirmation form whose action really does submit to production), so
# nothing found here is allowed to slip through just because it wasn't an
# <a href> or <form action>. Concretely, this app's shared delete/approve/
# reject modals set their form's `action` at click time via Alpine
# (`x-on:click="$dispatch('set-delete', {action: 'https://real-domain/...'})"`
# on the row, `x-on:set-delete.window="$el.action = $event.detail.action"` on
# the modal) - restoring real Alpine.js (needed for dropdowns/sidebar
# submenus to work at all) means that dispatch payload is live and would
# otherwise really submit there. Same risk pattern for a stray favicon/
# lazy-image url() this build never had a rule for. Domain-agnostic on
# purpose - covers the app's own domain AND any third-party host (S3/CDN
# image buckets, blog subdomains) with no extra rules to keep in sync.
EXTERNAL_URL_IN_ATTR_RE = re.compile(r"https?://[^\s'\"<>)]+")


def neutralize_external_refs_everywhere(soup):
    """Replace every remaining http(s) URL substring in every attribute of
    every tag with '#' - run this LAST, after every more targeted/faithful
    localization pass has already had a chance to resolve or vendor what it
    recognizes. Only ever narrows what's left (never touches an already-
    localized relative path, since those don't contain '://')."""
    count = 0
    for tag in soup.find_all(True):
        if tag.attrs is None:
            continue
        for attr, value in list(tag.attrs.items()):
            if not isinstance(value, str) or "://" not in value:
                continue
            new_value, n = EXTERNAL_URL_IN_ATTR_RE.subn("#", value)
            if n:
                tag[attr] = new_value
                count += n
    return count


def neutralize_domain_in_text(soup, domain):
    """Some pages display a live URL as its own content, not just as a link
    target - a "your landing page's public URL" table cell, an embed-code
    snippet shown as an example - already-safe href/action handling doesn't
    touch that (it's just text, not an attribute). No live request happens
    either way, but showing "https://#" there would read as broken output;
    swapping the domain itself for an obviously-fake local placeholder (not
    stripping the whole URL) keeps the mockup readable while not displaying
    a real, working link to the live/testing domain anywhere. Plain-text
    brand-name mentions with no scheme (a support-ticket message, an
    "@handle" placeholder example) are left alone - those aren't links and
    carry no such implication."""
    if not domain:
        return 0
    pattern = re.compile(r"(https?://)((?:[a-zA-Z0-9-]+\.)*)" + re.escape(domain) + r"\b")
    count = 0
    for node in soup.find_all(string=pattern):
        new_text, n = pattern.subn(r"\g<1>\g<2>mockup.local", str(node))
        if n:
            node.replace_with(new_text)
            count += n
    return count


def relink_existing_mockups(route_map, just_built_id):
    """Run after every build: sweep all OTHER previously-generated mockups
    for links that couldn't be resolved at the time (data-mockup-unresolved)
    and re-check them against the now-current route map. This is what makes
    the whole set self-healing as new pages get added - build the "detail"
    page today and every earlier mockup's dead "Detail" button starts working
    without re-running anything for those pages."""
    stats = Counter()
    if not PAGES_DIR.exists():
        return stats

    for module_dir in sorted(PAGES_DIR.iterdir()):
        if not module_dir.is_dir() or module_dir.name.startswith("_"):
            continue
        for html_path in sorted(module_dir.glob("*.html")):
            module, page = module_dir.name, html_path.stem
            if page_id(module, page) == just_built_id:
                continue
            html = html_path.read_text(encoding="utf-8", errors="ignore")
            if "data-mockup-unresolved" not in html:
                continue

            soup = BeautifulSoup(html, "lxml")
            changed = False
            for tag in soup.find_all(attrs={"data-mockup-unresolved": True}):
                path = tag["data-mockup-unresolved"]
                target = resolve_route(path, route_map, self_id=page_id(module, page))
                if not target:
                    continue
                target_module, target_page = target.split("/", 1)
                attr = "href" if tag.has_attr("href") else "action"
                tag[attr] = relative_link(module, target_module, target_page)
                del tag["data-mockup-unresolved"]
                changed = True
                stats["links_relinked"] += 1

            if changed:
                html_path.write_text(str(soup), encoding="utf-8")
                stats["pages_updated"] += 1

    return stats


def rewrite_head_assets(soup, out_dir, capture_assets_dir):
    stats = Counter()

    captured_hrefs, captured_stats = vendor_captured_stylesheets(soup, out_dir, capture_assets_dir)
    stats.update(captured_stats)

    head = ensure_head(soup)
    if captured_hrefs:
        # Ground-truth CSS from the real page - use it as-is, don't also mix
        # in the (possibly stale) QUANTUM bundle to avoid cascade conflicts.
        for href in captured_hrefs:
            head.append(soup.new_tag("link", rel="stylesheet", href=href))
        stats["render_css_source"] = f"captured ({len(captured_hrefs)} file(s))"
    else:
        # No capture available (e.g. a mockup built from scratch) - best
        # effort: fall back to whatever QUANTUM bundle is in the local repo.
        vendored_href, vendor_stats = vendor_quantum_css(out_dir)
        stats.update(vendor_stats)
        if vendored_href:
            head.append(soup.new_tag("link", rel="stylesheet", href=vendored_href))
            stats["render_css_source"] = f"QUANTUM fallback ({vendored_href}) - may be stale, no capture to verify against"

    if capture_assets_dir is not None:
        def vendor_image(fname):
            """Copy fname from the raw capture's own _files folder into
            THIS module's _assets/captured-images/ (shared/deduped across
            every page in the module, same as captured CSS) and return the
            new relative href - never a path back into mockups/raw/, which
            is intake scratch space, not something pages/ should depend on
            existing at open-time (zip up pages/<module>/ on its own, move
            it, delete raw/ later - it must still render). A curated asset
            (mockups/assets/<fname>) wins over the capture's own copy for
            the "user" (public site) module only - a lazy-load pattern's
            "real" src there is often just a tiny blur-up placeholder stub,
            not the actual hero image. Scoped to this one module on purpose:
            the exact same filename ('default.webp') is coincidentally also
            a generic QUANTUM empty-state/broken-logo icon in the admin
            panels - unrelated image, unrelated meaning, so a filename match
            there must NOT pull in the public site's hero photo instead."""
            if not fname:
                return None  # e.g. a dynamic '/api/?query=...' src with no path segment to vendor
            curated = CURATED_ASSETS_DIR / fname if out_dir.name == "user" else None
            src = curated if curated and curated.is_file() else capture_assets_dir / fname
            if not src.is_file():
                return None
            dest_dir = out_dir / "_assets" / "captured-images"
            dest = dest_dir / fname
            # Re-copy if a curated asset exists but wasn't the source used
            # last time (e.g. this filename first got vendored from a raw
            # capture's placeholder, before mockups/assets/<fname> existed).
            if not dest.exists() or (curated and curated.is_file() and dest.stat().st_size != curated.stat().st_size):
                dest_dir.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, dest)
            return f"_assets/captured-images/{fname}"

        for tag in soup.find_all(["img"], src=True):
            fname = tag["src"].split("/")[-1]
            href = vendor_image(fname)
            if href:
                tag["src"] = href
                stats["images_repointed_to_capture"] += 1

        # Lazy-load pattern (src = tiny placeholder or absent, data-src = the
        # real image) - now actually read by the restored lazy-load engine
        # (see app-BbkPvvSm.js in FUNCTIONAL_SCRIPTS), so this is no longer
        # write-once-ignored: if the real image is a first-party capture
        # asset, localize it the same as a plain <img src>; a per-user
        # avatar generated by ui-avatars.com (no static filename to vendor -
        # it's an API call, not a file) gets the curated profile.webp
        # instead of either leaving a live external call or an empty image;
        # anything else is inevitably remote per-record content (an
        # uploaded gallery/brochure photo, a CMS thumbnail) with no local
        # equivalent - drop the attribute rather than leave a live external
        # URL in the markup.
        for tag in soup.find_all(attrs={"data-src": True}):
            data_src = tag["data-src"]
            if "ui-avatars.com" in data_src:
                href = vendor_image("profile.webp")
                if href:
                    tag["data-src"] = href
                    tag["src"] = href
                    stats["images_repointed_to_capture"] += 1
                    continue
            fname = data_src.split("/")[-1].split("?")[0]
            href = vendor_image(fname)
            if href:
                tag["data-src"] = href
                stats["images_repointed_to_capture"] += 1
            elif data_src.startswith(("http://", "https://")):
                del tag["data-src"]
                stats["external_urls_dropped"] += 1

        # Favicon is almost never saved by "Save Complete" (it's fetched by
        # the browser chrome, not the page) - fall back to the capture's own
        # logo rather than leave it pointing at the live/testing domain.
        # Filename varies per app, so try every logo-shaped file this tool
        # has seen bundled with a capture, not just one hardcoded name.
        fallback_logo = next(
            (f for f in (
                "logo-sevimaplatform-small.png", "logo-sevima-platform.png",
                "sevima-logo.webp", "mk-crm-logo-mini.webp",
            ) if (capture_assets_dir / f).exists()),
            None,
        )
        for tag in soup.find_all("link", rel="icon"):
            fname = tag.get("href", "").split("/")[-1]
            href = vendor_image(fname) if fname else None
            if href:
                tag["href"] = href
            elif fallback_logo:
                tag["href"] = vendor_image(fallback_logo)
                stats["favicon_replaced_with_local_logo"] += 1
            else:
                # No local stand-in at all (nothing about a missing favicon
                # is user-visible) - drop it rather than leave it pointing
                # at the live/testing domain.
                tag.decompose()
                stats["external_urls_dropped"] += 1

    return stats


INTERACTION_LABELS = {
    "dropdown": "Dropdowns (navbar menus, filter pickers, etc.)",
    "collapse": "Collapse panels (navbar toggler, accordions, filter drawers)",
    "modal": "Modals",
    "offcanvas": "Offcanvas panels",
    "tab": "Tabs", "pill": "Pills",
    "destructive-confirm": "Delete/hapus buttons (real confirmation modal from the capture, then row removed)",
}


def detect_interactions(soup):
    """What data-bs-*/data-* components does this page actually use? Drives
    the manifest's Interactions section so it's obvious what got wired up
    versus what simply isn't present on this particular page. Two
    conventions are merged here (Bootstrap's data-bs-toggle and the newer
    QUANTUM revision's bare data-toggle) since a given page only ever uses
    one of them - see the two independent IIFEs in INTERACTIONS_JS."""
    counts = Counter()
    for tag in soup.find_all(attrs={"data-bs-toggle": True}):
        counts[tag["data-bs-toggle"]] += 1
    for tag in soup.find_all(attrs={"data-toggle": True}):
        counts[tag["data-toggle"]] += 1
    alert_dismiss = len(soup.find_all(attrs={"data-bs-dismiss": "alert"}))
    if alert_dismiss:
        counts["alert-dismiss"] = alert_dismiss
    destructive = (
        len(soup.find_all(attrs={"data-mockup-confirm": True}))
        + len(soup.find_all(attrs={"data-mockup-delete-row-trigger": True}))
        + len(soup.find_all(attrs={"data-mockup-bulk-delete": True}))
    )
    if destructive:
        counts["destructive-confirm"] = destructive
    return counts


def classify_classes(soup, known_classes):
    counter = Counter()
    for tag in soup.find_all(True):
        if tag.attrs is None:
            continue
        for c in tag.get("class") or []:
            counter[c] += 1

    matched, sym_icons, bootstrap_utility, qn_drift, other = [], [], [], [], []
    for cls, count in counter.items():
        if cls in NOISE_CLASS_TOKENS:
            continue
        prefix = cls.split("-")[0]
        if cls in known_classes:
            matched.append((cls, count))
        elif cls == "sym" or cls.startswith("sym-"):
            sym_icons.append((cls, count))
        elif cls.startswith("qn-") or cls.startswith("qn_"):
            qn_drift.append((cls, count))
        elif prefix in BOOTSTRAP_UTILITY_PREFIXES:
            bootstrap_utility.append((cls, count))
        else:
            other.append((cls, count))

    for bucket in (matched, sym_icons, bootstrap_utility, qn_drift, other):
        bucket.sort(key=lambda x: (-x[1], x[0]))

    return {
        "matched_quantum": matched,
        "sym_icons": sym_icons,
        "bootstrap_utility": bootstrap_utility,
        "qn_drift": qn_drift,
        "other_unclassified": other,
    }


def find_colors(soup, reverse_lookup):
    mapped, unmapped = [], []
    seen = set()
    texts = [tag["style"] for tag in soup.find_all(style=True)]
    texts += [t.string or "" for t in soup.find_all("style")]
    for text in texts:
        for hexval in HEX_COLOR_RE.findall(text or ""):
            key = hexval.lower()
            if key in seen:
                continue
            seen.add(key)
            token = reverse_lookup.get(key)
            (mapped if token else unmapped).append((hexval, token))
    return mapped, unmapped


def render_manifest(slug, raw_path, out_html, cleanup_stats, head_stats, classes, colors, interactions,
                     pending_paths, relink_stats):
    mapped_colors, unmapped_colors = colors
    lines = []
    lines.append(f"# Mockup sync report - {slug}")
    lines.append("")
    if head_stats.get("module_warning"):
        lines.append(f"> ⚠️ **{head_stats['module_warning']}**")
        lines.append("")
    lines.append(f"- Source capture: `{raw_path.relative_to(ROOT).as_posix()}`")
    lines.append(f"- Generated mockup: `{out_html.relative_to(ROOT).as_posix()}`")
    lines.append(f"- Rendering CSS source: **{head_stats.get('render_css_source', 'NONE FOUND')}**")
    if "captured" in head_stats.get("render_css_source", ""):
        lines.append("  (this page's own captured stylesheet was used, so visuals should match production exactly)")
    elif head_stats.get("assets_copied") is not None:
        lines.append(f"  ({head_stats.get('assets_copied', 0)} fonts/icons copied from QUANTUM, "
                      f"{head_stats.get('assets_not_found', 0)} referenced but not found - may render slightly off)")
    lines.append(f"- Everything is local now - {head_stats.get('local_assets_matched', 0)} font/pattern url()s "
                  f"resolved to first-party QUANTUM files (`quantum-symbols`, header/sidebar patterns), "
                  f"{head_stats.get('external_urls_dropped', 0)} unresolvable external url()s dropped to `none`.")
    lines.append("")

    neutralized = head_stats.get("external_refs_neutralized", 0)
    text_neutralized = head_stats.get("domain_text_mentions_neutralized", 0)
    lines.append("## Production/testing domain safety check")
    lines.append("")
    if neutralized:
        lines.append(f"- ⚠️ **{neutralized}** reference(s) to a live http(s) URL were found OUTSIDE the usual "
                      f"`<a href>`/`<form action>`/`<img src>` handling above - typically a URL embedded as a "
                      f"string literal inside an inline JS attribute (`x-on:click=\"$dispatch(...)\"`, `onclick`, "
                      f"a lazy-load `data-src`, a dynamically-set form `action`) - and replaced with `#`. This is "
                      f"what stops a destructive action (delete/approve/reject, etc.) that a real Alpine.js "
                      f"handler restored by this tool might otherwise actually submit to the live/testing "
                      f"backend. **No live domain should remain anywhere in this file** - if you spot one "
                      f"`view-source:` didn't catch, treat it as a bug in `neutralize_external_refs_everywhere`.")
    else:
        lines.append("- No stray external URLs found outside the usual href/action/src handling.")
    if text_neutralized:
        lines.append(f"- **{text_neutralized}** more mention(s) of the live domain shown as plain TEXT (not a "
                      f"link/attribute - e.g. a \"copy this landing page URL\" cell, an embed-code example) had "
                      f"just the domain swapped for `mockup.local` - no active risk either way (nothing there "
                      f"was ever clickable/submittable), just so nothing on the page reads as a real production "
                      f"address.")
    lines.append("")

    lines.append("## Internal navigation")
    lines.append("")
    lines.append(f"- Links pointing to other app pages that already have a mockup built: "
                  f"**{head_stats.get('internal_links_resolved', 0)}** - rewritten to open that mockup directly "
                  f"(navbar tabs, \"Tambah\"/Edit/Detail buttons, etc. actually navigate, same as production).")
    if pending_paths:
        lines.append(f"- Links with no matching mockup yet: **{head_stats.get('internal_links_pending', 0)}** - "
                      f"left as `#` for now. Capture one of these pages next and re-run the build (any slug) to "
                      f"wire them up automatically, on this page AND every other mockup that links to it:")
        lines.append("")
        for path in pending_paths:
            lines.append(f"  - `{path}`")
    else:
        lines.append("- No pending links - every internal link on this page already has a matching mockup.")
    if relink_stats.get("pages_updated"):
        lines.append("")
        lines.append(f"- Building this page also fixed **{relink_stats['links_relinked']}** previously-dead link(s) "
                      f"across **{relink_stats['pages_updated']}** earlier mockup(s) that were waiting for this "
                      f"route to exist.")
    lines.append("")

    lines.append("## Interactions")
    lines.append("")
    if interactions:
        lines.append("Detected on this page and wired up via `mockup-interactions.js` "
                      "(a small local re-implementation covering both the Bootstrap 5 `data-bs-*` contract and "
                      "the newer QUANTUM `data-toggle`/`data-target`/`data-dismiss` contract - the real production "
                      "JS bundle isn't reusable from a static capture, but the CSS state classes each drives are "
                      "the same ones already in the captured stylesheet, so behavior matches production):")
        lines.append("")
        for kind, count in sorted(interactions.items()):
            label = INTERACTION_LABELS.get(kind, kind)
            lines.append(f"- {label}: **{count}** trigger(s)")
        if head_stats.get("livewire_restored"):
            lines.append("- Sidebar submenus / modal content population driven by real Alpine.js directives "
                          "(`x-data`/`x-show`/`x-on`/`$dispatch`): the actual captured Livewire bundle (which "
                          "ships Alpine) was restored locally, so these work natively rather than being "
                          "reimplemented here.")
    else:
        lines.append("No `data-bs-toggle`/`data-toggle`/`data-dismiss` components detected on this page.")
    lines.append("")
    lines.append(f"Charts: {head_stats.get('functional_scripts_vendored', 0)} functional script(s) vendored "
                  f"locally (Chart.js + datalabels plugin + chart-settings) and the real inline chart-init "
                  f"script (with its actual data) was preserved - charts render for real, not a static image.")
    lines.append("")
    lines.append("**Create/update flash alerts**: a `.alert` that's already in the captured DOM will display and "
                  "dismiss correctly (see Interactions above). But an alert that only appears *after* submitting a "
                  "real create/update form can't be triggered here - there's no backend. If pixel-perfect "
                  "before/after states matter, capture the page again right after triggering that alert in the "
                  "real app, and re-run this script.")
    lines.append("")

    lines.append("## Cleanup")
    lines.append("")
    for key, label in [
        ("script_tags_removed", "`<script>` tags removed"),
        ("extension_tags_removed", "Browser-extension injected tags removed"),
        ("debug_toolbar_blocks_removed", "Debug toolbar / var-dump blocks removed"),
        ("livewire_alpine_attrs_removed", "`wire:*` attributes stripped (x-data/x-init are kept - see Interactions)"),
        ("framework_glue_attrs_removed", "Turbo/CSRF/Livewire-wiring attributes stripped (dead weight for slicing)"),
        ("chart_canvas_styles_cleared", "Stale Chart.js-computed `style` cleared off `<canvas>` (recomputed on load)"),
        ("preload_links_removed", "Preload/prefetch links removed"),
        ("noise_style_blocks_removed", "Dead/extension `<style>` blocks removed"),
        ("comments_removed", "HTML comments stripped"),
    ]:
        lines.append(f"- {label}: {cleanup_stats.get(key, 0)}")
    lines.append(f"- Captured `<link rel=stylesheet>` dropped (replaced by the vendored copies above): "
                  f"{head_stats.get('captured_stylesheets_dropped', 0)}")
    lines.append(f"- Captured `<script src>` dropped: {head_stats.get('captured_scripts_dropped', 0)} "
                  f"({head_stats.get('functional_scripts_vendored', 0)} of those kept - see Charts/Dropdowns above)")
    lines.append(f"- Images re-pointed to the local capture's asset folder: "
                  f"{head_stats.get('images_repointed_to_capture', 0)}")
    if head_stats.get("favicon_replaced_with_local_logo"):
        lines.append("- Favicon swapped for the capture's own logo (browsers don't save the real favicon file)")
    lines.append("")

    lines.append("## Classes found in this page vs. the local QUANTUM copy")
    lines.append("")
    lines.append(f"- Matched known QUANTUM classes: **{len(classes['matched_quantum'])}**")
    lines.append(f"- `sym-*` icon classes referenced: **{len(classes['sym_icons'])}**")
    lines.append(f"- Bootstrap-style utility classes: **{len(classes['bootstrap_utility'])}**")
    lines.append(f"- `qn-*` classes NOT found in local QUANTUM copy (possible drift): "
                  f"**{len(classes['qn_drift'])}**")
    lines.append(f"- Other/unclassified (likely app-specific, one-off): **{len(classes['other_unclassified'])}**")
    lines.append("")

    if classes["qn_drift"]:
        lines.append("### ⚠️ Possible design-system drift")
        lines.append("")
        lines.append("These look like QUANTUM component classes (`qn-` prefix) but weren't found in "
                      "any local QUANTUM checkout (`QUANTUM/quantum`, `QUANTUM/quantum-monorepo`, or "
                      "`QUANTUM/quantum-ai/source/quantum-v3.4`). Either every local copy is behind the "
                      "live app, or these were built ad-hoc and should be proposed back to QUANTUM as a "
                      "`[Suggestion]` issue (see `QUANTUM/quantum/README.md` - use "
                      "`/label ~\"suggestion\" ~\"component\"`).")
        lines.append("")
        for cls, count in classes["qn_drift"]:
            lines.append(f"- `{cls}` ({count}x)")
        lines.append("")

    if classes["sym_icons"]:
        lines.append("### Icon classes used (`sym-*`)")
        lines.append("")
        for cls, count in classes["sym_icons"]:
            lines.append(f"- `{cls}` ({count}x)")
        lines.append("")

    if classes["other_unclassified"]:
        lines.append("### Other / app-specific classes (review manually)")
        lines.append("")
        for cls, count in classes["other_unclassified"][:40]:
            lines.append(f"- `{cls}` ({count}x)")
        if len(classes["other_unclassified"]) > 40:
            lines.append(f"- ... and {len(classes['other_unclassified']) - 40} more")
        lines.append("")

    lines.append("## Colors")
    lines.append("")
    if mapped_colors:
        lines.append("Raw hex values that already have a matching QUANTUM token - replace with "
                      "`var(--token-name)` instead of the hardcoded hex:")
        lines.append("")
        for hexval, token in mapped_colors:
            lines.append(f"- `{hexval}` -> `var({token})`")
        lines.append("")
    if unmapped_colors:
        lines.append("Raw hex values with **no** matching QUANTUM token (review with the design team "
                      "before reusing):")
        lines.append("")
        for hexval, _ in unmapped_colors:
            lines.append(f"- `{hexval}`")
        lines.append("")
    if not mapped_colors and not unmapped_colors:
        lines.append("No hardcoded hex colors found in inline styles - good, this page relies on "
                      "QUANTUM classes/tokens only.")
        lines.append("")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    raw_arg = Path(sys.argv[1])
    raw_path = raw_arg if raw_arg.is_absolute() else (MOCKUPS / "raw" / raw_arg)
    if not raw_path.exists():
        # allow passing just a filename that lives directly under mockups/raw/**
        matches = list((MOCKUPS / "raw").rglob(raw_arg.name))
        if len(matches) == 1:
            raw_path = matches[0]
        else:
            print(f"Could not resolve raw html file: {sys.argv[1]}")
            sys.exit(1)

    module, page = parse_target(raw_path, sys.argv[2] if len(sys.argv) > 2 else None)
    pid = page_id(module, page)
    out_dir = PAGES_DIR / module
    out_dir.mkdir(parents=True, exist_ok=True)
    out_html = out_dir / f"{page}.html"
    out_manifest = out_dir / f"{page}.manifest.md"

    tokens_data = load_json(TOKENS_DIR / "design-tokens.json")
    classes_data = load_json(TOKENS_DIR / "component-classes.json")
    known_classes = set(classes_data["classes"].keys())
    reverse_lookup = tokens_data["reverse_color_lookup"]

    html = raw_path.read_text(encoding="utf-8", errors="ignore")
    html = PRE_PARSE_STRIP_RE.sub("", html)
    html = ALPINE_AT_SHORTHAND_RE.sub(r"x-on:\1=", html)
    soup = BeautifulSoup(html, "lxml")

    route_map = load_route_map()
    capture_path = extract_capture_path(html)
    if capture_path:
        route_map[pid] = {"module": module, "page": page, "path": capture_path,
                           "pattern": path_pattern(capture_path)}
        save_route_map(route_map)
    suggested_module = suggest_module(capture_path)
    module_mismatch = bool(suggested_module and suggested_module != module)
    module_warning = None
    if module_mismatch:
        module_warning = (
            f"Captured URL `{capture_path}` looks like it belongs to module **{suggested_module}**, "
            f"but this page was built as `{module}/{page}`. If other pages of that module already "
            f"exist, rebuild this one as `{suggested_module}/{page}` so they share one folder "
            f"instead of sitting isolated in their own."
        )
        print(f"WARNING: {module_warning}")

    # A page can genuinely execute a script it only ever hinted at via
    # <link rel=modulepreload> (a Vite entry importing a chunk through its
    # own module graph, never a second literal <script src=...> for it) -
    # has to be read BEFORE strip_noise drops every preload/modulepreload
    # link as noise, or the evidence that this page really uses it is gone.
    modulepreload_matches = [
        (fname, match)
        for tag in soup.find_all("link", rel="modulepreload")
        for fname in [tag.get("href", "").split("/")[-1]]
        for match in [next((clean for raw, clean in FUNCTIONAL_SCRIPTS if raw == fname), None)]
        if match
    ]

    cleanup_stats, kept_inline_scripts = strip_noise(soup)
    capture_assets_dir = find_capture_assets_dir(raw_path)
    head_stats = rewrite_head_assets(soup, out_dir, capture_assets_dir)
    head_stats.update(restore_functional_scripts(
        soup, out_dir, capture_assets_dir, kept_inline_scripts, modulepreload_matches))
    head_stats.update(localize_inline_styles(soup, out_dir))
    link_stats, pending_paths = resolve_internal_links(soup, module, page, route_map)
    if page_id(module, page) in AUTH_PAGES or module == "preferences":
        # Livewire enables the submit button once the fields are filled; with
        # no backend it would stay disabled forever, so enable it here (native
        # `required` validation still applies on submit).
        for btn in soup.select('form button[type="submit"][disabled]'):
            del btn["disabled"]
        # A static server answers POST with 405, so "submit" just navigates
        # to the form's action (the user area) after native validation passes.
        for form in soup.find_all("form", action=True):
            form["onsubmit"] = "event.preventDefault();location.href=this.getAttribute('action')"
        if page_id(module, page) in AUTH_PAGES and soup.head is not None:
            style = soup.new_tag("style")
            style.string = AUTH_LAYOUT_CSS
            soup.head.append(style)
    head_stats.update(link_stats)
    if module_warning:
        head_stats["module_warning"] = module_warning
    classes = classify_classes(soup, known_classes)
    colors = find_colors(soup, reverse_lookup)
    interactions = detect_interactions(soup)

    # Final safety net - see neutralize_external_refs_everywhere's docstring.
    # Must run after every other pass above (they resolve/vendor what they
    # recognize into local paths first; this only ever mops up what's left).
    head_stats["external_refs_neutralized"] = neutralize_external_refs_everywhere(soup)
    capture_domain = extract_capture_domain(html)
    head_stats["domain_text_mentions_neutralized"] = neutralize_domain_in_text(soup, capture_domain)

    out_html.write_text(str(soup), encoding="utf-8")
    relink_stats = relink_existing_mockups(route_map, just_built_id=pid)
    out_manifest.write_text(
        render_manifest(pid, raw_path, out_html, cleanup_stats, head_stats, classes, colors, interactions,
                         pending_paths, relink_stats),
        encoding="utf-8",
    )

    print(f"Mockup written to {out_html.relative_to(ROOT)}")
    print(f"Manifest written to {out_manifest.relative_to(ROOT)}")
    print(f"Quantum classes matched: {len(classes['matched_quantum'])}, "
          f"drift candidates: {len(classes['qn_drift'])}, "
          f"unclassified: {len(classes['other_unclassified'])}")
    print(f"Internal links resolved: {link_stats.get('internal_links_resolved', 0)}, "
          f"pending: {link_stats.get('internal_links_pending', 0)}, "
          f"older mockups relinked: {relink_stats.get('links_relinked', 0)}")
    if not capture_path:
        print("Note: this capture has no 'saved from url=' comment (probably made via "
              "Copy outerHTML, not Save Complete) - internal navigation can't be wired for it.")


if __name__ == "__main__":
    main()