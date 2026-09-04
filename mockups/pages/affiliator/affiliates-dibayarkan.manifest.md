# Mockup sync report - affiliator/affiliates-dibayarkan

- Source capture: `mockups/raw/maukuliah_affiliator/Sevima CRM _ Dibayar Afiliasi Saya.html`
- Generated mockup: `mockups/pages/affiliator/affiliates-dibayarkan.html`
- Rendering CSS source: **captured (4 file(s))**
  (this page's own captured stylesheet was used, so visuals should match production exactly)
- Everything is local now - 0 font/pattern url()s resolved to first-party QUANTUM files (`quantum-symbols`, header/sidebar patterns), 0 unresolvable external url()s dropped to `none`.

## Production/testing domain safety check

- No stray external URLs found outside the usual href/action/src handling.

## Internal navigation

- Links pointing to other app pages that already have a mockup built: **18** - rewritten to open that mockup directly (navbar tabs, "Tambah"/Edit/Detail buttons, etc. actually navigate, same as production).
- Links with no matching mockup yet: **14** - left as `#` for now. Capture one of these pages next and re-run the build (any slug) to wire them up automatically, on this page AND every other mockup that links to it:

  - `/628123456789`
  - `/628123456890`
  - `/affiliator/notifications`
  - `/affiliator/notifications/mark-all-as-read`
  - `/affiliator/notifications/read/103aacd2-2d37-4757-befc-3b44901f289a`
  - `/affiliator/notifications/read/5b7dc113-7776-46a6-aad2-e76593739f75`
  - `/affiliator/notifications/read/b6b85ed6-9a5f-497d-9c44-b2bb6d244e05`
  - `/affiliator/notifications/read/e6daddac-3d6f-4c83-bdfd-c0cb8b5c41cf`
  - `/affiliator/notifications/read/f70d4f49-9786-469d-af61-881969c14449`
  - `/affiliator/onboarding`
  - `/logout`

## Interactions

Detected on this page and wired up via `mockup-interactions.js` (a small local re-implementation covering both the Bootstrap 5 `data-bs-*` contract and the newer QUANTUM `data-toggle`/`data-target`/`data-dismiss` contract - the real production JS bundle isn't reusable from a static capture, but the CSS state classes each drives are the same ones already in the captured stylesheet, so behavior matches production):

- Dropdowns (navbar menus, filter pickers, etc.): **4** trigger(s)
- Modals: **1** trigger(s)
- Tabs: **1** trigger(s)
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
- Images re-pointed to the local capture's asset folder: 3
- Favicon swapped for the capture's own logo (browsers don't save the real favicon file)

## Classes found in this page vs. the local QUANTUM copy

- Matched known QUANTUM classes: **145**
- `sym-*` icon classes referenced: **0**
- Bootstrap-style utility classes: **14**
- `qn-*` classes NOT found in local QUANTUM copy (possible drift): **0**
- Other/unclassified (likely app-specific, one-off): **52**

### Other / app-specific classes (review manually)

- `items-center` (26x)
- `whitespace-nowrap` (10x)
- `choices__item--choice` (6x)
- `!text-blue-600` (5x)
- `cursor-pointer` (5x)
- `font-mono` (5x)
- `hover:bg-slate-200` (5x)
- `notification__avatar` (5x)
- `size-8` (5x)
- `!font-medium` (4x)
- `!rounded-full` (4x)
- `!grid` (2x)
- `!hidden` (2x)
- `-right-2` (2x)
- `-top-2` (2x)
- `absolute` (2x)
- `avatar__acronym` (2x)
- `header__row-wrapper` (2x)
- `md:!flex` (2x)
- `!bg-black/10` (1x)
- `!border-white/50` (1x)
- `!p-0` (1x)
- `!rounded-lg` (1x)
- `!text-white` (1x)
- `animate-ping` (1x)
- `antialiased` (1x)
- `choices__input--cloned` (1x)
- `choices__list--single` (1x)
- `entered` (1x)
- `gf-app` (1x)
- `give-freely-root` (1x)
- `grid-cols-1` (1x)
- `grid-cols-12` (1x)
- `header__identity-sub` (1x)
- `header__identity-wrapper` (1x)
- `header__row-wrapper_nav` (1x)
- `header__switch-avatar` (1x)
- `header__switch-avatar-name` (1x)
- `header_template` (1x)
- `lazy` (1x)
- ... and 12 more

## Colors

Raw hex values with **no** matching QUANTUM token (review with the design team before reusing):

- `#22c55e`
- `#fff`
- `#2299dd`
- `#29d`
