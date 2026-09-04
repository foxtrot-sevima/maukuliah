# Mockup sync report - super-admin/log-modules

- Source capture: `mockups/raw/maukuliah_super_admin/Sevima CRM _ Log Penggunaan Modul Fitur.html`
- Generated mockup: `mockups/pages/super-admin/log-modules.html`
- Rendering CSS source: **captured (4 file(s))**
  (this page's own captured stylesheet was used, so visuals should match production exactly)
- Everything is local now - 0 font/pattern url()s resolved to first-party QUANTUM files (`quantum-symbols`, header/sidebar patterns), 0 unresolvable external url()s dropped to `none`.

## Production/testing domain safety check

- No stray external URLs found outside the usual href/action/src handling.

## Internal navigation

- Links pointing to other app pages that already have a mockup built: **51** - rewritten to open that mockup directly (navbar tabs, "Tambah"/Edit/Detail buttons, etc. actually navigate, same as production).
- Links with no matching mockup yet: **23** - left as `#` for now. Capture one of these pages next and re-run the build (any slug) to wire them up automatically, on this page AND every other mockup that links to it:

  - `/logout`
  - `/super-admin/log/accesses`
  - `/super-admin/log/applications`
  - `/super-admin/log/modules/add-affiliator`
  - `/super-admin/log/modules/add-prospect-log`
  - `/super-admin/log/modules/assign-agent-prospect`
  - `/super-admin/log/modules/delete-prospect`
  - `/super-admin/log/modules/edit-prospect`
  - `/super-admin/log/modules/export-prospect`
  - `/super-admin/log/modules/export-riasec-registrar`
  - `/super-admin/log/modules/import-prospect`
  - `/super-admin/log/modules/print-payment-history-affiliate`
  - `/super-admin/log/modules/update-prospect`
  - `/super-admin/log/modules/update-status-prospect`
  - `/super-admin/log/modules/validate-affiliate`
  - `/super-admin/log/modules/view-detail-prospect`
  - `/super-admin/log/modules/view-learning-style-test-registrar`
  - `/super-admin/log/modules/view-list-prospect`
  - `/super-admin/log/modules/view-mbti-test-registrar`
  - `/super-admin/log/modules/view-riasec-registrar`
  - `/super-admin/settings`

## Interactions

Detected on this page and wired up via `mockup-interactions.js` (a small local re-implementation covering both the Bootstrap 5 `data-bs-*` contract and the newer QUANTUM `data-toggle`/`data-target`/`data-dismiss` contract - the real production JS bundle isn't reusable from a static capture, but the CSS state classes each drives are the same ones already in the captured stylesheet, so behavior matches production):

- Dropdowns (navbar menus, filter pickers, etc.): **10** trigger(s)
- Modals: **1** trigger(s)
- Sidebar submenus / modal content population driven by real Alpine.js directives (`x-data`/`x-show`/`x-on`/`$dispatch`): the actual captured Livewire bundle (which ships Alpine) was restored locally, so these work natively rather than being reimplemented here.

Charts: 2 functional script(s) vendored locally (Chart.js + datalabels plugin + chart-settings) and the real inline chart-init script (with its actual data) was preserved - charts render for real, not a static image.

**Create/update flash alerts**: a `.alert` that's already in the captured DOM will display and dismiss correctly (see Interactions above). But an alert that only appears *after* submitting a real create/update form can't be triggered here - there's no backend. If pixel-perfect before/after states matter, capture the page again right after triggering that alert in the real app, and re-run this script.

## Cleanup

- `<script>` tags removed: 3
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
- Images re-pointed to the local capture's asset folder: 32
- Favicon swapped for the capture's own logo (browsers don't save the real favicon file)

## Classes found in this page vs. the local QUANTUM copy

- Matched known QUANTUM classes: **144**
- `sym-*` icon classes referenced: **0**
- Bootstrap-style utility classes: **10**
- `qn-*` classes NOT found in local QUANTUM copy (possible drift): **0**
- Other/unclassified (likely app-specific, one-off): **45**

### Other / app-specific classes (review manually)

- `items-center` (42x)
- `font-semibold` (33x)
- `choices__item--choice` (20x)
- `hover:text-blue-600` (18x)
- `hover:bg-blue-100` (17x)
- `items-start` (17x)
- `whitespace-nowrap` (17x)
- `lazy` (15x)
- `divide-dashed` (11x)
- `divide-y` (11x)
- `entered` (5x)
- `loaded` (5x)
- `size-10` (5x)
- `!font-medium` (4x)
- `!grid` (2x)
- `avatar__acronym` (2x)
- `header__row-wrapper` (2x)
- `!p-0` (1x)
- `antialiased` (1x)
- `choices__input--cloned` (1x)
- `choices__list--single` (1x)
- `cursor-pointer` (1x)
- `duration-500` (1x)
- `gf-app` (1x)
- `give-freely-root` (1x)
- `grid-cols-1` (1x)
- `grid-cols-2` (1x)
- `header__identity-sub` (1x)
- `header__identity-wrapper` (1x)
- `header__row-wrapper_nav` (1x)
- `header__sidebar-nav_simple` (1x)
- `header__switch-avatar` (1x)
- `header__switch-avatar-name` (1x)
- `header_template` (1x)
- `hover:bg-slate-100` (1x)
- `lg:grid-cols-2` (1x)
- `lg:order-first` (1x)
- `lg:w-max` (1x)
- `modal__title` (1x)
- `nav_template` (1x)
- ... and 5 more

## Colors

Raw hex values with **no** matching QUANTUM token (review with the design team before reusing):

- `#2299dd`
- `#29d`
