# Mockup sync report - user/majors

> ⚠️ **Captured URL `/majors` looks like it belongs to module **majors**, but this page was built as `user/majors`. If other pages of that module already exist, rebuild this one as `majors/majors` so they share one folder instead of sitting isolated in their own.**

- Source capture: `mockups/raw/maukuliah_user/Maukuliah _ Jurusan.html`
- Generated mockup: `mockups/pages/user/majors.html`
- Rendering CSS source: **captured (2 file(s))**
  (this page's own captured stylesheet was used, so visuals should match production exactly)
- Everything is local now - 0 font/pattern url()s resolved to first-party QUANTUM files (`quantum-symbols`, header/sidebar patterns), 16 unresolvable external url()s dropped to `none`.

## Production/testing domain safety check

- ⚠️ **62** reference(s) to a live http(s) URL were found OUTSIDE the usual `<a href>`/`<form action>`/`<img src>` handling above - typically a URL embedded as a string literal inside an inline JS attribute (`x-on:click="$dispatch(...)"`, `onclick`, a lazy-load `data-src`, a dynamically-set form `action`) - and replaced with `#`. This is what stops a destructive action (delete/approve/reject, etc.) that a real Alpine.js handler restored by this tool might otherwise actually submit to the live/testing backend. **No live domain should remain anywhere in this file** - if you spot one `view-source:` didn't catch, treat it as a bug in `neutralize_external_refs_everywhere`.

## Internal navigation

- Links pointing to other app pages that already have a mockup built: **57** - rewritten to open that mockup directly (navbar tabs, "Tambah"/Edit/Detail buttons, etc. actually navigate, same as production).
- Links with no matching mockup yet: **38** - left as `#` for now. Capture one of these pages next and re-run the build (any slug) to wire them up automatically, on this page AND every other mockup that links to it:

  - `/@maukuliah.id`
  - `/channel/UCef7ROjIxoECo49TqafFThA`
  - `/crm`
  - `/faq`
  - `/favourites`
  - `/logout`
  - `/majors/data-science`
  - `/majors/ekonomi`
  - `/majors/geografi`
  - `/majors/ilmu-komputer`
  - `/majors/ilmu-politik`
  - `/majors/konservasi-sumber-daya-alam`
  - `/majors/lingkungan-hidup`
  - `/majors/linguistik`
  - `/majors/meteorologi`
  - `/majors/oseanografi`
  - `/majors/pengelolaan-limbah`
  - `/majors/politik-dan-pemerintahan`
  - `/majors/sastra-daerah`
  - `/majors/sastra-inggris`
  - `/majors/sastra-jepang`
  - `/majors/teknologi-informasi`
  - `/maukuliah.id`
  - `/maukuliah.id/`
  - `/tryouts/history`
  - `/universities/institut-sains-dan-teknologi-nasional`
  - `/universities/universitas-haji-sumatera-utara`
  - `/universities/universitas-pasundan`

## Interactions

No `data-bs-toggle`/`data-toggle`/`data-dismiss` components detected on this page.

Charts: 3 functional script(s) vendored locally (Chart.js + datalabels plugin + chart-settings) and the real inline chart-init script (with its actual data) was preserved - charts render for real, not a static image.

**Create/update flash alerts**: a `.alert` that's already in the captured DOM will display and dismiss correctly (see Interactions above). But an alert that only appears *after* submitting a real create/update form can't be triggered here - there's no backend. If pixel-perfect before/after states matter, capture the page again right after triggering that alert in the real app, and re-run this script.

## Cleanup

- `<script>` tags removed: 3
- Browser-extension injected tags removed: 0
- Debug toolbar / var-dump blocks removed: 0
- `wire:*` attributes stripped (x-data/x-init are kept - see Interactions): 90
- Turbo/CSRF/Livewire-wiring attributes stripped (dead weight for slicing): 1
- Stale Chart.js-computed `style` cleared off `<canvas>` (recomputed on load): 0
- Preload/prefetch links removed: 4
- Dead/extension `<style>` blocks removed: 1
- HTML comments stripped: 8
- Captured `<link rel=stylesheet>` dropped (replaced by the vendored copies above): 2
- Captured `<script src>` dropped: 3 (3 of those kept - see Charts/Dropdowns above)
- Images re-pointed to the local capture's asset folder: 25

## Classes found in this page vs. the local QUANTUM copy

- Matched known QUANTUM classes: **39**
- `sym-*` icon classes referenced: **0**
- Bootstrap-style utility classes: **63**
- `qn-*` classes NOT found in local QUANTUM copy (possible drift): **0**
- Other/unclassified (likely app-specific, one-off): **134**

### Other / app-specific classes (review manually)

- `items-center` (91x)
- `font-medium` (63x)
- `font-semibold` (49x)
- `cursor-pointer` (31x)
- `lazy` (27x)
- `md:text-base` (25x)
- `group` (23x)
- `hover:border-maukuliah-400` (23x)
- `relative` (23x)
- `absolute` (22x)
- `line-clamp-1` (22x)
- `hover:bg-neutral-300` (21x)
- `md:text-lg` (21x)
- `transition-all` (19x)
- `animate-pulse` (18x)
- `underline` (18x)
- `md:p-4` (17x)
- `group-hover:brightness-75` (16x)
- `hidden` (16x)
- `hover:bg-maukuliah-100` (16x)
- `left-2` (16x)
- `line-clamp-2` (16x)
- `line-clamp-3` (16x)
- `md:gap-4` (16x)
- `md:h-[200px]` (16x)
- `min-h-[100px]` (16x)
- `mr-2` (16x)
- `focus:ring-2` (15x)
- `focus:ring-maukuliah-400` (15x)
- `entered` (14x)
- `font-bold` (8x)
- `inline-flex` (8x)
- `fixed` (7x)
- `-translate-y-1/2` (6x)
- `group-hover:text-maukuliah-400` (6x)
- `hover:bg-maukuliah-400/10` (6x)
- `group-hover:fill-maukuliah-400` (5x)
- `left-0` (5x)
- `lg:hidden` (5x)
- `md:p-0` (5x)
- ... and 94 more

## Colors

Raw hex values with **no** matching QUANTUM token (review with the design team before reusing):

- `#2299dd`
- `#29d`
