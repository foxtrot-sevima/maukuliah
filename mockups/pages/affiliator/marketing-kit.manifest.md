# Mockup sync report - affiliator/marketing-kit

> ⚠️ **Captured URL `/universities/universitas-sentra-vidya-utama/DES11` looks like it belongs to module **universities**, but this page was built as `affiliator/marketing-kit`. If other pages of that module already exist, rebuild this one as `universities/marketing-kit` so they share one folder instead of sitting isolated in their own.**

- Source capture: `mockups/raw/maukuliah_affiliator/Sevima CRM _ Marketing Kit.html`
- Generated mockup: `mockups/pages/affiliator/marketing-kit.html`
- Rendering CSS source: **captured (3 file(s))**
  (this page's own captured stylesheet was used, so visuals should match production exactly)
- Everything is local now - 0 font/pattern url()s resolved to first-party QUANTUM files (`quantum-symbols`, header/sidebar patterns), 0 unresolvable external url()s dropped to `none`.

## Production/testing domain safety check

- ⚠️ **1** reference(s) to a live http(s) URL were found OUTSIDE the usual `<a href>`/`<form action>`/`<img src>` handling above - typically a URL embedded as a string literal inside an inline JS attribute (`x-on:click="$dispatch(...)"`, `onclick`, a lazy-load `data-src`, a dynamically-set form `action`) - and replaced with `#`. This is what stops a destructive action (delete/approve/reject, etc.) that a real Alpine.js handler restored by this tool might otherwise actually submit to the live/testing backend. **No live domain should remain anywhere in this file** - if you spot one `view-source:` didn't catch, treat it as a bug in `neutralize_external_refs_everywhere`.

## Internal navigation

- Links pointing to other app pages that already have a mockup built: **2** - rewritten to open that mockup directly (navbar tabs, "Tambah"/Edit/Detail buttons, etc. actually navigate, same as production).
- Links with no matching mockup yet: **6** - left as `#` for now. Capture one of these pages next and re-run the build (any slug) to wire them up automatically, on this page AND every other mockup that links to it:

  - `/628123456789`
  - `/privacy-policy`
  - `/terms-and-condition`
  - `/universities/universitas-sentra-vidya-utama`
  - `/universities/universitas-sentra-vidya-utama/brochures/download-no-auth`

## Interactions

No `data-bs-toggle`/`data-toggle`/`data-dismiss` components detected on this page.

Charts: 2 functional script(s) vendored locally (Chart.js + datalabels plugin + chart-settings) and the real inline chart-init script (with its actual data) was preserved - charts render for real, not a static image.

**Create/update flash alerts**: a `.alert` that's already in the captured DOM will display and dismiss correctly (see Interactions above). But an alert that only appears *after* submitting a real create/update form can't be triggered here - there's no backend. If pixel-perfect before/after states matter, capture the page again right after triggering that alert in the real app, and re-run this script.

## Cleanup

- `<script>` tags removed: 0
- Browser-extension injected tags removed: 0
- Debug toolbar / var-dump blocks removed: 0
- `wire:*` attributes stripped (x-data/x-init are kept - see Interactions): 0
- Turbo/CSRF/Livewire-wiring attributes stripped (dead weight for slicing): 1
- Stale Chart.js-computed `style` cleared off `<canvas>` (recomputed on load): 0
- Preload/prefetch links removed: 4
- Dead/extension `<style>` blocks removed: 1
- HTML comments stripped: 7
- Captured `<link rel=stylesheet>` dropped (replaced by the vendored copies above): 3
- Captured `<script src>` dropped: 3 (2 of those kept - see Charts/Dropdowns above)
- Images re-pointed to the local capture's asset folder: 7
- Favicon swapped for the capture's own logo (browsers don't save the real favicon file)

## Classes found in this page vs. the local QUANTUM copy

- Matched known QUANTUM classes: **30**
- `sym-*` icon classes referenced: **0**
- Bootstrap-style utility classes: **16**
- `qn-*` classes NOT found in local QUANTUM copy (possible drift): **0**
- Other/unclassified (likely app-specific, one-off): **37**

### Other / app-specific classes (review manually)

- `!font-medium` (5x)
- `!rounded-full` (5x)
- `entered` (3x)
- `items-center` (3x)
- `lazy` (3x)
- `loaded` (3x)
- `hover:underline` (2x)
- `!max-w-[150px]` (1x)
- `!object-contain` (1x)
- `!w-[100px]` (1x)
- `!w-full` (1x)
- `absolute` (1x)
- `advanced-login__form` (1x)
- `antialiased` (1x)
- `body` (1x)
- `divide-x` (1x)
- `font-bold` (1x)
- `font-medium` (1x)
- `footer-login` (1x)
- `footer-login__language` (1x)
- `footer-login__logo` (1x)
- `footer-login__text` (1x)
- `from-blue-900` (1x)
- `gf-app` (1x)
- `give-freely-root` (1x)
- `header-login` (1x)
- `header-login__logo` (1x)
- `header-login__name` (1x)
- `header-login__separator` (1x)
- `main_advanced-login` (1x)
- `max-w-screen-sm` (1x)
- `relative` (1x)
- `right-0` (1x)
- `scroll-smooth` (1x)
- `selection:bg-blue-100` (1x)
- `selection:text-blue-600` (1x)
- `to-slate-900` (1x)

## Colors

Raw hex values with **no** matching QUANTUM token (review with the design team before reusing):

- `#2299dd`
- `#29d`
