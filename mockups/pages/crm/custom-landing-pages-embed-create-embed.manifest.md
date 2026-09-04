# Mockup sync report - crm/custom-landing-pages-embed-create-embed

- Source capture: `mockups/raw/maukuliah_crm/Sevima CRM _ Buat Sematan Tracker Landing Page.html`
- Generated mockup: `mockups/pages/crm/custom-landing-pages-embed-create-embed.html`
- Rendering CSS source: **captured (4 file(s))**
  (this page's own captured stylesheet was used, so visuals should match production exactly)
- Everything is local now - 0 font/pattern url()s resolved to first-party QUANTUM files (`quantum-symbols`, header/sidebar patterns), 0 unresolvable external url()s dropped to `none`.

## Production/testing domain safety check

- No stray external URLs found outside the usual href/action/src handling.

## Internal navigation

- Links pointing to other app pages that already have a mockup built: **34** - rewritten to open that mockup directly (navbar tabs, "Tambah"/Edit/Detail buttons, etc. actually navigate, same as production).
- Links with no matching mockup yet: **10** - left as `#` for now. Capture one of these pages next and re-run the build (any slug) to wire them up automatically, on this page AND every other mockup that links to it:

  - `/crm/affiliates/validate`
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

- Dropdowns (navbar menus, filter pickers, etc.): **10** trigger(s)
- Tabs: **1** trigger(s)
- Sidebar submenus / modal content population driven by real Alpine.js directives (`x-data`/`x-show`/`x-on`/`$dispatch`): the actual captured Livewire bundle (which ships Alpine) was restored locally, so these work natively rather than being reimplemented here.

Charts: 2 functional script(s) vendored locally (Chart.js + datalabels plugin + chart-settings) and the real inline chart-init script (with its actual data) was preserved - charts render for real, not a static image.

**Create/update flash alerts**: a `.alert` that's already in the captured DOM will display and dismiss correctly (see Interactions above). But an alert that only appears *after* submitting a real create/update form can't be triggered here - there's no backend. If pixel-perfect before/after states matter, capture the page again right after triggering that alert in the real app, and re-run this script.

## Cleanup

- `<script>` tags removed: 2
- Browser-extension injected tags removed: 0
- Debug toolbar / var-dump blocks removed: 0
- `wire:*` attributes stripped (x-data/x-init are kept - see Interactions): 22
- Turbo/CSRF/Livewire-wiring attributes stripped (dead weight for slicing): 1
- Stale Chart.js-computed `style` cleared off `<canvas>` (recomputed on load): 0
- Preload/prefetch links removed: 4
- Dead/extension `<style>` blocks removed: 1
- HTML comments stripped: 6
- Captured `<link rel=stylesheet>` dropped (replaced by the vendored copies above): 4
- Captured `<script src>` dropped: 4 (2 of those kept - see Charts/Dropdowns above)
- Images re-pointed to the local capture's asset folder: 7
- Favicon swapped for the capture's own logo (browsers don't save the real favicon file)

## Classes found in this page vs. the local QUANTUM copy

- Matched known QUANTUM classes: **124**
- `sym-*` icon classes referenced: **0**
- Bootstrap-style utility classes: **25**
- `qn-*` classes NOT found in local QUANTUM copy (possible drift): **0**
- Other/unclassified (likely app-specific, one-off): **54**

### Other / app-specific classes (review manually)

- `hidden` (9x)
- `peer` (9x)
- `focus:ring-blue-600` (8x)
- `hover:ring-blue-600` (8x)
- `items-center` (8x)
- `ring-2` (8x)
- `ring-neutral-300` (8x)
- `peer-checked:ring-blue-600` (6x)
- `!text-blue-600` (5x)
- `hover:bg-slate-200` (5x)
- `notification__avatar` (5x)
- `size-8` (5x)
- `absolute` (3x)
- `ml-auto` (3x)
- `relative` (3x)
- `!font-medium` (2x)
- `!hidden` (2x)
- `-right-2` (2x)
- `-top-2` (2x)
- `avatar__acronym` (2x)
- `duration-500` (2x)
- `entered` (2x)
- `header__row-wrapper` (2x)
- `lazy` (2x)
- `loaded` (2x)
- `md:!flex` (2x)
- `peer-checked:bg-blue-50` (2x)
- `peer-checked:border-blue-600` (2x)
- `peer-checked:text-blue-600` (2x)
- `transition-all` (2x)
- `!border-white/50` (1x)
- `!grid` (1x)
- `!h-0` (1x)
- `!p-0` (1x)
- `!rounded-lg` (1x)
- `!w-0` (1x)
- `animate-ping` (1x)
- `antialiased` (1x)
- `disabled` (1x)
- `font-medium` (1x)
- ... and 14 more

## Colors

Raw hex values with **no** matching QUANTUM token (review with the design team before reusing):

- `#2299dd`
- `#29d`
