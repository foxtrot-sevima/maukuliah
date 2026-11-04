# Mockup sync report - login/index

- Source capture: `mockups/raw/maukuliah_auth/Sevima CRM _ Login.html`
- Generated mockup: `mockups/pages/login/index.html`
- Rendering CSS source: **captured (3 file(s))**
  (this page's own captured stylesheet was used, so visuals should match production exactly)
- Everything is local now - 0 font/pattern url()s resolved to first-party QUANTUM files (`quantum-symbols`, header/sidebar patterns), 0 unresolvable external url()s dropped to `none`.

## Production/testing domain safety check

- No stray external URLs found outside the usual href/action/src handling.

## Internal navigation

- Links pointing to other app pages that already have a mockup built: **4** - rewritten to open that mockup directly (navbar tabs, "Tambah"/Edit/Detail buttons, etc. actually navigate, same as production).
- Links with no matching mockup yet: **3** - left as `#` for now. Capture one of these pages next and re-run the build (any slug) to wire them up automatically, on this page AND every other mockup that links to it:

  - `/password/reset`
  - `/privacy-policy`
  - `/terms-and-condition`

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
- Dead/extension `<style>` blocks removed: 0
- HTML comments stripped: 7
- Captured `<link rel=stylesheet>` dropped (replaced by the vendored copies above): 3
- Captured `<script src>` dropped: 3 (2 of those kept - see Charts/Dropdowns above)
- Images re-pointed to the local capture's asset folder: 6
- Favicon swapped for the capture's own logo (browsers don't save the real favicon file)

## Classes found in this page vs. the local QUANTUM copy

- Matched known QUANTUM classes: **33**
- `sym-*` icon classes referenced: **0**
- Bootstrap-style utility classes: **5**
- `qn-*` classes NOT found in local QUANTUM copy (possible drift): **0**
- Other/unclassified (likely app-specific, one-off): **40**

### Other / app-specific classes (review manually)

- `!font-medium` (2x)
- `entered` (2x)
- `hover:underline` (2x)
- `items-center` (2x)
- `lazy` (2x)
- `loaded` (2x)
- `!max-w-[150px]` (1x)
- `!object-contain` (1x)
- `!w-[100px]` (1x)
- `advanced-login__form` (1x)
- `advanced-login__illustration` (1x)
- `advanced-login__illustration-image` (1x)
- `advanced-login__separator` (1x)
- `advanced-login__separator-bottom` (1x)
- `advanced-login__separator-bottom-corner-bottom` (1x)
- `advanced-login__separator-bottom-corner-middle` (1x)
- `advanced-login__separator-bottom-corner-top` (1x)
- `advanced-login__separator-top` (1x)
- `advanced-login__separator-top-corner-bottom` (1x)
- `advanced-login__separator-top-corner-middle` (1x)
- `advanced-login__separator-top-corner-top` (1x)
- `advanced-login__wrapper` (1x)
- `antialiased` (1x)
- `body` (1x)
- `divide-x` (1x)
- `footer-login` (1x)
- `footer-login__language` (1x)
- `footer-login__logo` (1x)
- `footer-login__text` (1x)
- `form_action-area` (1x)
- `header-login` (1x)
- `header-login__logo` (1x)
- `header-login__name` (1x)
- `header-login__separator` (1x)
- `main_advanced-login` (1x)
- `relative` (1x)
- `scroll-smooth` (1x)
- `selection:bg-blue-100` (1x)
- `selection:text-blue-600` (1x)
- `size-6` (1x)

## Colors

Raw hex values with **no** matching QUANTUM token (review with the design team before reusing):

- `#2299dd`
- `#29d`
