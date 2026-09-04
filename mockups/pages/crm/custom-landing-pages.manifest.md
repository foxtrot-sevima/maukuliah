# Mockup sync report - crm/custom-landing-pages

- Source capture: `mockups/raw/maukuliah_crm/Sevima CRM _ Tracker & Landing Page.html`
- Generated mockup: `mockups/pages/crm/custom-landing-pages.html`
- Rendering CSS source: **captured (4 file(s))**
  (this page's own captured stylesheet was used, so visuals should match production exactly)
- Everything is local now - 0 font/pattern url()s resolved to first-party QUANTUM files (`quantum-symbols`, header/sidebar patterns), 0 unresolvable external url()s dropped to `none`.

## Production/testing domain safety check

- ⚠️ **20** reference(s) to a live http(s) URL were found OUTSIDE the usual `<a href>`/`<form action>`/`<img src>` handling above - typically a URL embedded as a string literal inside an inline JS attribute (`x-on:click="$dispatch(...)"`, `onclick`, a lazy-load `data-src`, a dynamically-set form `action`) - and replaced with `#`. This is what stops a destructive action (delete/approve/reject, etc.) that a real Alpine.js handler restored by this tool might otherwise actually submit to the live/testing backend. **No live domain should remain anywhere in this file** - if you spot one `view-source:` didn't catch, treat it as a bug in `neutralize_external_refs_everywhere`.
- **10** more mention(s) of the live domain shown as plain TEXT (not a link/attribute - e.g. a "copy this landing page URL" cell, an embed-code example) had just the domain swapped for `mockup.local` - no active risk either way (nothing there was ever clickable/submittable), just so nothing on the page reads as a real production address.

## Internal navigation

- Links pointing to other app pages that already have a mockup built: **113** - rewritten to open that mockup directly (navbar tabs, "Tambah"/Edit/Detail buttons, etc. actually navigate, same as production).
- Links with no matching mockup yet: **13** - left as `#` for now. Capture one of these pages next and re-run the build (any slug) to wire them up automatically, on this page AND every other mockup that links to it:

  - `/crm/affiliates/validate`
  - `/crm/custom-landing-pages/create`
  - `/crm/custom-landing-pages/embed/daftar-sekarang-pada-webiste-utama/edit`
  - `/crm/notifications`
  - `/crm/notifications/mark-all-as-read`
  - `/crm/notifications/read/0cef242b-261a-40ee-b364-2c9cbe0ac9ef`
  - `/crm/notifications/read/4c97d8b4-3e4e-45da-a518-32165e486ee7`
  - `/crm/notifications/read/e56eac70-ec49-4b93-ba17-f883b2bd6607`
  - `/crm/notifications/read/f07c6af0-bef2-45ad-84f5-5e0b27519e42`
  - `/crm/notifications/read/f3f06c53-1232-4142-9578-47171ed17245`
  - `/logout`
  - `/super-admin/settings`

## Interactions

Detected on this page and wired up via `mockup-interactions.js` (a small local re-implementation covering both the Bootstrap 5 `data-bs-*` contract and the newer QUANTUM `data-toggle`/`data-target`/`data-dismiss` contract - the real production JS bundle isn't reusable from a static capture, but the CSS state classes each drives are the same ones already in the captured stylesheet, so behavior matches production):

- Dropdowns (navbar menus, filter pickers, etc.): **30** trigger(s)
- Modals: **13** trigger(s)
- Tabs: **1** trigger(s)
- Sidebar submenus / modal content population driven by real Alpine.js directives (`x-data`/`x-show`/`x-on`/`$dispatch`): the actual captured Livewire bundle (which ships Alpine) was restored locally, so these work natively rather than being reimplemented here.

Charts: 2 functional script(s) vendored locally (Chart.js + datalabels plugin + chart-settings) and the real inline chart-init script (with its actual data) was preserved - charts render for real, not a static image.

**Create/update flash alerts**: a `.alert` that's already in the captured DOM will display and dismiss correctly (see Interactions above). But an alert that only appears *after* submitting a real create/update form can't be triggered here - there's no backend. If pixel-perfect before/after states matter, capture the page again right after triggering that alert in the real app, and re-run this script.

## Cleanup

- `<script>` tags removed: 5
- Browser-extension injected tags removed: 0
- Debug toolbar / var-dump blocks removed: 0
- `wire:*` attributes stripped (x-data/x-init are kept - see Interactions): 0
- Turbo/CSRF/Livewire-wiring attributes stripped (dead weight for slicing): 1
- Stale Chart.js-computed `style` cleared off `<canvas>` (recomputed on load): 0
- Preload/prefetch links removed: 4
- Dead/extension `<style>` blocks removed: 1
- HTML comments stripped: 6
- Captured `<link rel=stylesheet>` dropped (replaced by the vendored copies above): 4
- Captured `<script src>` dropped: 4 (2 of those kept - see Charts/Dropdowns above)
- Images re-pointed to the local capture's asset folder: 3
- Favicon swapped for the capture's own logo (browsers don't save the real favicon file)

## Classes found in this page vs. the local QUANTUM copy

- Matched known QUANTUM classes: **191**
- `sym-*` icon classes referenced: **0**
- Bootstrap-style utility classes: **21**
- `qn-*` classes NOT found in local QUANTUM copy (possible drift): **0**
- Other/unclassified (likely app-specific, one-off): **68**

### Other / app-specific classes (review manually)

- `items-center` (53x)
- `whitespace-nowrap` (17x)
- `!font-medium` (11x)
- `line-clamp-1` (10x)
- `choices__item--choice` (9x)
- `!max-h-8` (8x)
- `!max-w-8` (8x)
- `!min-h-8` (8x)
- `!min-w-8` (8x)
- `font-semibold` (8x)
- `hover:bg-blue-100` (7x)
- `!text-blue-600` (5x)
- `hover:bg-slate-200` (5x)
- `ml-auto` (5x)
- `notification__avatar` (5x)
- `size-8` (5x)
- `group` (4x)
- `modal__title` (4x)
- `!flex` (3x)
- `!grid` (3x)
- `cursor-pointer` (3x)
- `disabled` (3x)
- `duration-500` (3x)
- `font-medium` (3x)
- `hover:border-blue-600` (3x)
- `line-clamp-2` (3x)
- `size-4` (3x)
- `transition-all` (3x)
- `!hidden` (2x)
- `-right-2` (2x)
- `-top-2` (2x)
- `absolute` (2x)
- `avatar__acronym` (2x)
- `choices__input--cloned` (2x)
- `choices__list--single` (2x)
- `grid-cols-1` (2x)
- `header__row-wrapper` (2x)
- `lg:grid-cols-2` (2x)
- `lg:order-first` (2x)
- `md:!flex` (2x)
- ... and 28 more

## Colors

Raw hex values with **no** matching QUANTUM token (review with the design team before reusing):

- `#2299dd`
- `#29d`
