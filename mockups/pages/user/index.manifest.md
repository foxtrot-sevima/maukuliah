# Mockup sync report - user/index

- Source capture: `mockups/raw/maukuliah_user/Maukuliah _ Temukan Informasi Kampus dan Jurusan Terlengkap.html`
- Generated mockup: `mockups/pages/user/index.html`
- Rendering CSS source: **captured (3 file(s))**
  (this page's own captured stylesheet was used, so visuals should match production exactly)
- Everything is local now - 0 font/pattern url()s resolved to first-party QUANTUM files (`quantum-symbols`, header/sidebar patterns), 13 unresolvable external url()s dropped to `none`.

## Production/testing domain safety check

- ⚠️ **82** reference(s) to a live http(s) URL were found OUTSIDE the usual `<a href>`/`<form action>`/`<img src>` handling above - typically a URL embedded as a string literal inside an inline JS attribute (`x-on:click="$dispatch(...)"`, `onclick`, a lazy-load `data-src`, a dynamically-set form `action`) - and replaced with `#`. This is what stops a destructive action (delete/approve/reject, etc.) that a real Alpine.js handler restored by this tool might otherwise actually submit to the live/testing backend. **No live domain should remain anywhere in this file** - if you spot one `view-source:` didn't catch, treat it as a bug in `neutralize_external_refs_everywhere`.

## Internal navigation

- Links pointing to other app pages that already have a mockup built: **81** - rewritten to open that mockup directly (navbar tabs, "Tambah"/Edit/Detail buttons, etc. actually navigate, same as production).
- Links with no matching mockup yet: **65** - left as `#` for now. Capture one of these pages next and re-run the build (any slug) to wire them up automatically, on this page AND every other mockup that links to it:

  - `/10-website-ai-yang-perlu-diketahui-oleh-mahasiswa/`
  - `/6-cara-menemukan-passion-untuk-memilih-jurusan-kuliah/`
  - `/@maukuliah.id`
  - `/bedah-interview-hr-dan-user-apa-bedanya/`
  - `/calon-mahasiswa-baru-ini-cara-sistem-penilaian-utbk-snbt-2024/`
  - `/channel/UCef7ROjIxoECo49TqafFThA`
  - `/crm`
  - `/faq`
  - `/favourites`
  - `/jobs/agen-pariwisata-1`
  - `/jobs/ahli-kepatuhan-compliance`
  - `/jobs/ahli-pelayanan-pelanggan`
  - `/jobs/insinyur-struktural`
  - `/jobs/konsultan-transportasi-1`
  - `/jobs/mediator`
  - `/jobs/music-director`
  - `/jobs/pengembang-perangkat-lunak-kesehatan`
  - `/logout`
  - `/majors/administrasi-fiskal`
  - `/majors/antropologi-budaya`
  - `/majors/ilmu-falak`
  - `/majors/manajemen`
  - `/majors/oseanografi`
  - `/majors/sastra-jerman`
  - `/majors/tata-rias-dan-kecantikan`
  - `/majors/teknologi-rekayasa-manufaktur`
  - `/maukuliah.id`
  - `/maukuliah.id/`
  - `/regions`
  - `/scholarships/beasiswa-dies-natalis-ulbi`
  - `/scholarships/beasiswa-prestasi-daerah-provinsi`
  - `/scholarships/beasiswa-stba-jia-2026-kuliah-bisa-gratis`
  - `/scholarships/tahfidz-pendalaman-kitab-suci-ulbi-2026`
  - `/tryouts/history`
  - `/universities/akademi-komunitas-industri-tekstil-dan-produk-tekstil-surakarta`
  - `/universities/indonesia-international-institute-for-life-sciences`
  - `/universities/institut-sains-dan-teknologi-nasional`
  - `/universities/politeknik-negeri-tanah-laut`
  - `/universities/sekolah-tinggi-ilmu-hukum-iblam`
  - `/universities/sekolah-tinggi-teologi-baptis-indonesia`
  - `/universities/stkip-agama-hindu-amlapura`
  - `/universities/universitas-haji-sumatera-utara`
  - `/universities/universitas-islam-batik`
  - `/universities/universitas-matana`
  - `/universities/universitas-pasundan`
  - `/universities/universitas-sembilanbelas-november-kolaka`

## Interactions

No `data-bs-toggle`/`data-toggle`/`data-dismiss` components detected on this page.

Charts: 3 functional script(s) vendored locally (Chart.js + datalabels plugin + chart-settings) and the real inline chart-init script (with its actual data) was preserved - charts render for real, not a static image.

**Create/update flash alerts**: a `.alert` that's already in the captured DOM will display and dismiss correctly (see Interactions above). But an alert that only appears *after* submitting a real create/update form can't be triggered here - there's no backend. If pixel-perfect before/after states matter, capture the page again right after triggering that alert in the real app, and re-run this script.

## Cleanup

- `<script>` tags removed: 6
- Browser-extension injected tags removed: 0
- Debug toolbar / var-dump blocks removed: 0
- `wire:*` attributes stripped (x-data/x-init are kept - see Interactions): 26
- Turbo/CSRF/Livewire-wiring attributes stripped (dead weight for slicing): 1
- Stale Chart.js-computed `style` cleared off `<canvas>` (recomputed on load): 0
- Preload/prefetch links removed: 4
- Dead/extension `<style>` blocks removed: 1
- HTML comments stripped: 8
- Captured `<link rel=stylesheet>` dropped (replaced by the vendored copies above): 3
- Captured `<script src>` dropped: 5 (3 of those kept - see Charts/Dropdowns above)
- Images re-pointed to the local capture's asset folder: 123

## Classes found in this page vs. the local QUANTUM copy

- Matched known QUANTUM classes: **44**
- `sym-*` icon classes referenced: **0**
- Bootstrap-style utility classes: **85**
- `qn-*` classes NOT found in local QUANTUM copy (possible drift): **0**
- Other/unclassified (likely app-specific, one-off): **187**

### Other / app-specific classes (review manually)

- `items-center` (102x)
- `font-semibold` (94x)
- `lazy` (86x)
- `font-medium` (66x)
- `entered` (62x)
- `hover:border-maukuliah-400` (56x)
- `hover:bg-maukuliah-100` (48x)
- `loaded` (48x)
- `md:text-lg` (47x)
- `transition-all` (46x)
- `group` (43x)
- `absolute` (41x)
- `line-clamp-2` (40x)
- `group-hover:brightness-75` (36x)
- `relative` (36x)
- `md:h-[200px]` (35x)
- `md:p-4` (35x)
- `md:gap-4` (34x)
- `md:text-base` (32x)
- `min-h-[100px]` (32x)
- `swiper-slide` (32x)
- `line-clamp-3` (28x)
- `font-bold` (26x)
- `hidden` (26x)
- `hover:bg-neutral-300` (23x)
- `items-start` (21x)
- `line-clamp-1` (21x)
- `left-2` (20x)
- `underline` (18x)
- `md:gap-2` (15x)
- `lg:hidden` (13x)
- `whitespace-nowrap` (13x)
- `md:h-9` (12x)
- `md:w-9` (12x)
- `md:p-0` (11x)
- `md:text-sm` (11x)
- `hover:brightness-75` (10x)
- `md:border-b-0` (10x)
- `hover:bg-maukuliah-400/10` (9x)
- `md:gap-8` (9x)
- ... and 147 more

## Colors

Raw hex values with **no** matching QUANTUM token (review with the design team before reusing):

- `#202b4a`
- `#2299dd`
- `#29d`
