# Self-hosted fonts

## Caveat

Used for the handwritten display accents across the UI — shopping list names,
notepad card headings, and section titles.

- **Source**: Google Fonts, family `Caveat`, version v23
- **License**: SIL Open Font License 1.1 — https://openfontlicense.org
- **Designer**: Impallari Type

Caveat is a variable font, so a single file per unicode subset covers weights
400–700; there is no separate file per weight.

| File | Subset |
|---|---|
| `caveat-latin.woff2` | latin (`U+0000-00FF` and friends) |
| `caveat-latin-ext.woff2` | latin-ext |

### Why self-hosted

The app is a PWA with an explicit offline mode (`composables/offlineComposable.js`).
Fonts pulled from `fonts.googleapis.com` at runtime fail when offline and leave the
handwritten styling — a signature part of the design — silently falling back. Bundling
them through Vite means they are cached by the service worker with the rest of the
assets and render the same offline as online.

The `@font-face` declarations live in `src/styles/fonts.css`, which points at these
files with relative URLs so Vite fingerprints them on build. The workbox config in
`vite.config.js` already precaches `woff2`, so they land in the service worker cache
with no extra setup.

### Updating

Re-download from Google Fonts with a modern browser user-agent to get woff2 (the
default UA yields legacy formats), then keep only the latin and latin-ext subsets:

```bash
curl -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36" \
  "https://fonts.googleapis.com/css2?family=Caveat:wght@400;600;700&display=swap"
```
