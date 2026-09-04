# Mockup sync report - user/riasec

> ⚠️ **Captured URL `/riasec` looks like it belongs to module **riasec**, but this page was built as `user/riasec`. If other pages of that module already exist, rebuild this one as `riasec/riasec` so they share one folder instead of sitting isolated in their own.**

- Source capture: `mockups/raw/maukuliah_user/Maukuliah _ Tes Minat Bakat.html`
- Generated mockup: `mockups/pages/user/riasec.html`
- Rendering CSS source: **captured (2 file(s))**
  (this page's own captured stylesheet was used, so visuals should match production exactly)
- Everything is local now - 0 font/pattern url()s resolved to first-party QUANTUM files (`quantum-symbols`, header/sidebar patterns), 1 unresolvable external url()s dropped to `none`.

## Production/testing domain safety check

- ⚠️ **25** reference(s) to a live http(s) URL were found OUTSIDE the usual `<a href>`/`<form action>`/`<img src>` handling above - typically a URL embedded as a string literal inside an inline JS attribute (`x-on:click="$dispatch(...)"`, `onclick`, a lazy-load `data-src`, a dynamically-set form `action`) - and replaced with `#`. This is what stops a destructive action (delete/approve/reject, etc.) that a real Alpine.js handler restored by this tool might otherwise actually submit to the live/testing backend. **No live domain should remain anywhere in this file** - if you spot one `view-source:` didn't catch, treat it as a bug in `neutralize_external_refs_everywhere`.

## Internal navigation

- Links pointing to other app pages that already have a mockup built: **12** - rewritten to open that mockup directly (navbar tabs, "Tambah"/Edit/Detail buttons, etc. actually navigate, same as production).
- Links with no matching mockup yet: **6** - left as `#` for now. Capture one of these pages next and re-run the build (any slug) to wire them up automatically, on this page AND every other mockup that links to it:

  - `/logout`
  - `/riasec/guide`
  - `/universities/institut-sains-dan-teknologi-nasional`
  - `/universities/universitas-haji-sumatera-utara`
  - `/universities/universitas-pasundan`

## Interactions

No `data-bs-toggle`/`data-toggle`/`data-dismiss` components detected on this page.

Charts: 2 functional script(s) vendored locally (Chart.js + datalabels plugin + chart-settings) and the real inline chart-init script (with its actual data) was preserved - charts render for real, not a static image.

**Create/update flash alerts**: a `.alert` that's already in the captured DOM will display and dismiss correctly (see Interactions above). But an alert that only appears *after* submitting a real create/update form can't be triggered here - there's no backend. If pixel-perfect before/after states matter, capture the page again right after triggering that alert in the real app, and re-run this script.

## Cleanup

- `<script>` tags removed: 3
- Browser-extension injected tags removed: 0
- Debug toolbar / var-dump blocks removed: 0
- `wire:*` attributes stripped (x-data/x-init are kept - see Interactions): 8
- Turbo/CSRF/Livewire-wiring attributes stripped (dead weight for slicing): 1
- Stale Chart.js-computed `style` cleared off `<canvas>` (recomputed on load): 0
- Preload/prefetch links removed: 4
- Dead/extension `<style>` blocks removed: 1
- HTML comments stripped: 8
- Captured `<link rel=stylesheet>` dropped (replaced by the vendored copies above): 2
- Captured `<script src>` dropped: 3 (2 of those kept - see Charts/Dropdowns above)
- Images re-pointed to the local capture's asset folder: 11

## Classes found in this page vs. the local QUANTUM copy

- Matched known QUANTUM classes: **29**
- `sym-*` icon classes referenced: **0**
- Bootstrap-style utility classes: **46**
- `qn-*` classes NOT found in local QUANTUM copy (possible drift): **0**
- Other/unclassified (likely app-specific, one-off): **73**

### Other / app-specific classes (review manually)

- `items-center` (28x)
- `font-semibold` (13x)
- `hidden` (12x)
- `font-medium` (10x)
- `hover:bg-neutral-300` (8x)
- `lazy` (7x)
- `entered` (4x)
- `loaded` (4x)
- `absolute` (3x)
- `hover:bg-maukuliah-400/10` (3x)
- `hover:border-maukuliah-400` (3x)
- `relative` (3x)
- `-translate-y-1/2` (2x)
- `break-all` (2x)
- `fixed` (2x)
- `font-bold` (2x)
- `grid-cols-1` (2x)
- `group` (2x)
- `lg:flex` (2x)
- `lg:hidden` (2x)
- `line-clamp-1` (2x)
- `md:flex` (2x)
- `md:p-0` (2x)
- `-translate-x-1/2` (1x)
- `-z-10` (1x)
- `animate-pulse` (1x)
- `antialiased` (1x)
- `backdrop-blur-sm` (1x)
- `button-logout` (1x)
- `cursor-pointer` (1x)
- `divide-neutral-300` (1x)
- `divide-y-2` (1x)
- `focus:border-maukuliah-400` (1x)
- `focus:ring-4` (1x)
- `focus:ring-maukuliah-400/10` (1x)
- `font-instrument` (1x)
- `gf-app` (1x)
- `give-freely-root` (1x)
- `grayscale` (1x)
- `group-hover:border-maukuliah-400` (1x)
- ... and 33 more

## Colors

Raw hex values with **no** matching QUANTUM token (review with the design team before reusing):

- `#2299dd`
- `#29d`
