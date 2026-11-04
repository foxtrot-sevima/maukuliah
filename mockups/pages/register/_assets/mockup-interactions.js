// Local Bootstrap-5-compatible interaction layer for this mockup.
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
