# Mockup sync report - crm/affiliates-payment-histories-inv07072026007-print

- Source capture: `mockups/raw/maukuliah_crm/Sevima CRM _ Cetak Riwayat Pembayaran.html`
- Generated mockup: `mockups/pages/crm/affiliates-payment-histories-inv07072026007-print.html`
- Rendering CSS source: **captured (3 file(s))**
  (this page's own captured stylesheet was used, so visuals should match production exactly)
- Everything is local now - 0 font/pattern url()s resolved to first-party QUANTUM files (`quantum-symbols`, header/sidebar patterns), 1 unresolvable external url()s dropped to `none`.

## Production/testing domain safety check

- No stray external URLs found outside the usual href/action/src handling.

## Internal navigation

- Links pointing to other app pages that already have a mockup built: **1** - rewritten to open that mockup directly (navbar tabs, "Tambah"/Edit/Detail buttons, etc. actually navigate, same as production).
- No pending links - every internal link on this page already has a matching mockup.

## Interactions

No `data-bs-toggle`/`data-toggle`/`data-dismiss` components detected on this page.

Charts: 2 functional script(s) vendored locally (Chart.js + datalabels plugin + chart-settings) and the real inline chart-init script (with its actual data) was preserved - charts render for real, not a static image.

**Create/update flash alerts**: a `.alert` that's already in the captured DOM will display and dismiss correctly (see Interactions above). But an alert that only appears *after* submitting a real create/update form can't be triggered here - there's no backend. If pixel-perfect before/after states matter, capture the page again right after triggering that alert in the real app, and re-run this script.

## Cleanup

- `<script>` tags removed: 1
- Browser-extension injected tags removed: 0
- Debug toolbar / var-dump blocks removed: 0
- `wire:*` attributes stripped (x-data/x-init are kept - see Interactions): 0
- Turbo/CSRF/Livewire-wiring attributes stripped (dead weight for slicing): 1
- Stale Chart.js-computed `style` cleared off `<canvas>` (recomputed on load): 0
- Preload/prefetch links removed: 4
- Dead/extension `<style>` blocks removed: 1
- HTML comments stripped: 6
- Captured `<link rel=stylesheet>` dropped (replaced by the vendored copies above): 3
- Captured `<script src>` dropped: 3 (2 of those kept - see Charts/Dropdowns above)
- Images re-pointed to the local capture's asset folder: 1

## Classes found in this page vs. the local QUANTUM copy

- Matched known QUANTUM classes: **26**
- `sym-*` icon classes referenced: **0**
- Bootstrap-style utility classes: **13**
- `qn-*` classes NOT found in local QUANTUM copy (possible drift): **0**
- Other/unclassified (likely app-specific, one-off): **20**

### Other / app-specific classes (review manually)

- `!grid` (10x)
- `grid-cols-2` (8x)
- `font-semibold` (7x)
- `items-center` (3x)
- `!font-medium` (2x)
- `font-bold` (2x)
- `grid-cols-1` (2x)
- `absolute` (1x)
- `antialiased` (1x)
- `gf-app` (1x)
- `give-freely-root` (1x)
- `max-w-[30cm]` (1x)
- `max-w-[75%]` (1x)
- `min-h-screen` (1x)
- `print:border-0` (1x)
- `print:hidden` (1x)
- `print:max-w-full` (1x)
- `relative` (1x)
- `scroll-smooth` (1x)
- `uppercase` (1x)

## Colors

Raw hex values with **no** matching QUANTUM token (review with the design team before reusing):

- `#2299dd`
- `#29d`
