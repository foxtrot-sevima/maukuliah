# Mockup sync report - user/universities

> ⚠️ **Captured URL `/universities` looks like it belongs to module **universities**, but this page was built as `user/universities`. If other pages of that module already exist, rebuild this one as `universities/universities` so they share one folder instead of sitting isolated in their own.**

- Source capture: `mockups/raw/maukuliah_user/Maukuliah _ Kampus.html`
- Generated mockup: `mockups/pages/user/universities.html`
- Rendering CSS source: **captured (3 file(s))**
  (this page's own captured stylesheet was used, so visuals should match production exactly)
- Everything is local now - 0 font/pattern url()s resolved to first-party QUANTUM files (`quantum-symbols`, header/sidebar patterns), 24 unresolvable external url()s dropped to `none`.

## Production/testing domain safety check

- ⚠️ **63** reference(s) to a live http(s) URL were found OUTSIDE the usual `<a href>`/`<form action>`/`<img src>` handling above - typically a URL embedded as a string literal inside an inline JS attribute (`x-on:click="$dispatch(...)"`, `onclick`, a lazy-load `data-src`, a dynamically-set form `action`) - and replaced with `#`. This is what stops a destructive action (delete/approve/reject, etc.) that a real Alpine.js handler restored by this tool might otherwise actually submit to the live/testing backend. **No live domain should remain anywhere in this file** - if you spot one `view-source:` didn't catch, treat it as a bug in `neutralize_external_refs_everywhere`.

## Internal navigation

- Links pointing to other app pages that already have a mockup built: **57** - rewritten to open that mockup directly (navbar tabs, "Tambah"/Edit/Detail buttons, etc. actually navigate, same as production).
- Links with no matching mockup yet: **38** - left as `#` for now. Capture one of these pages next and re-run the build (any slug) to wire them up automatically, on this page AND every other mockup that links to it:

  - `/@maukuliah.id`
  - `/channel/UCef7ROjIxoECo49TqafFThA`
  - `/crm`
  - `/faq`
  - `/favourites`
  - `/logout`
  - `/maukuliah.id`
  - `/maukuliah.id/`
  - `/tryouts/history`
  - `/universities/institut-agama-islam-ngawi-jawa-timur`
  - `/universities/institut-sains-dan-teknologi-nasional`
  - `/universities/politeknik-kesehatan-kemenkes-maluku`
  - `/universities/politeknik-kesehatan-yba-bandung`
  - `/universities/politeknik-manufaktur-ceper`
  - `/universities/sekolah-tinggi-agama-islam-al-hikmah`
  - `/universities/sekolah-tinggi-diakones-hkbp-balige`
  - `/universities/sekolah-tinggi-ilmu-kesehatan-bethesda-yakkum-yogyakarta`
  - `/universities/sekolah-tinggi-teknologi-angkatan-laut`
  - `/universities/stie-pariwisata-indonesia`
  - `/universities/universitas-haji-sumatera-utara`
  - `/universities/universitas-islam-negeri-imam-bonjol-padang`
  - `/universities/universitas-logistik-dan-bisnis-internasional`
  - `/universities/universitas-matana`
  - `/universities/universitas-pasundan`
  - `/universities/universitas-yos-soedarso`

## Interactions

No `data-bs-toggle`/`data-toggle`/`data-dismiss` components detected on this page.

Charts: 5 functional script(s) vendored locally (Chart.js + datalabels plugin + chart-settings) and the real inline chart-init script (with its actual data) was preserved - charts render for real, not a static image.

**Create/update flash alerts**: a `.alert` that's already in the captured DOM will display and dismiss correctly (see Interactions above). But an alert that only appears *after* submitting a real create/update form can't be triggered here - there's no backend. If pixel-perfect before/after states matter, capture the page again right after triggering that alert in the real app, and re-run this script.

## Cleanup

- `<script>` tags removed: 3
- Browser-extension injected tags removed: 0
- Debug toolbar / var-dump blocks removed: 0
- `wire:*` attributes stripped (x-data/x-init are kept - see Interactions): 85
- Turbo/CSRF/Livewire-wiring attributes stripped (dead weight for slicing): 1
- Stale Chart.js-computed `style` cleared off `<canvas>` (recomputed on load): 0
- Preload/prefetch links removed: 4
- Dead/extension `<style>` blocks removed: 1
- HTML comments stripped: 8
- Captured `<link rel=stylesheet>` dropped (replaced by the vendored copies above): 3
- Captured `<script src>` dropped: 5 (5 of those kept - see Charts/Dropdowns above)
- Images re-pointed to the local capture's asset folder: 54

## Classes found in this page vs. the local QUANTUM copy

- Matched known QUANTUM classes: **39**
- `sym-*` icon classes referenced: **0**
- Bootstrap-style utility classes: **65**
- `qn-*` classes NOT found in local QUANTUM copy (possible drift): **0**
- Other/unclassified (likely app-specific, one-off): **149**

### Other / app-specific classes (review manually)

- `items-center` (101x)
- `font-medium` (57x)
- `font-semibold` (51x)
- `lazy` (43x)
- `entered` (36x)
- `group` (23x)
- `hover:border-maukuliah-400` (23x)
- `relative` (23x)
- `absolute` (22x)
- `hover:bg-neutral-300` (21x)
- `md:text-lg` (21x)
- `cursor-pointer` (19x)
- `transition-all` (19x)
- `animate-pulse` (18x)
- `items-start` (18x)
- `underline` (18x)
- `md:p-4` (17x)
- `min-h-[40px]` (17x)
- `min-w-[40px]` (17x)
- `group-hover:brightness-75` (16x)
- `hidden` (16x)
- `hover:bg-maukuliah-100` (16x)
- `left-2` (16x)
- `line-clamp-2` (16x)
- `line-clamp-3` (16x)
- `md:gap-2` (16x)
- `md:gap-4` (16x)
- `md:h-9` (16x)
- `md:h-[200px]` (16x)
- `md:w-9` (16x)
- `min-h-[100px]` (16x)
- `loaded` (13x)
- `md:text-base` (12x)
- `focus:ring-2` (9x)
- `focus:ring-maukuliah-400` (9x)
- `font-bold` (8x)
- `inline-flex` (8x)
- `fixed` (7x)
- `-translate-y-1/2` (6x)
- `group-hover:text-maukuliah-400` (6x)
- ... and 109 more

## Colors

Raw hex values with **no** matching QUANTUM token (review with the design team before reusing):

- `#303030`
- `#2299dd`
- `#e5e7eb`
- `#29d`
