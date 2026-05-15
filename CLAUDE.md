# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Personal static website for Jichao Yang, deployed via GitHub Pages at `jichaoyang.com` (see `CNAME`). No build step, no JavaScript framework — just hand-written HTML/CSS served directly.

## Architecture

- `index.html` — top-level landing page with the navigation list (Blog / Projects / Code / Friends / Contact / Tufte CSS / Wrap). Each entry is a sibling subdirectory whose `index.html` is served when its path is visited.
- Subdirectories that are independent pages: `projects/`, `friends/`, `under_construction/` (placeholder for Blog), `wrap/` (a CSS text-wrapping demo, self-contained with its own `styles.css`).
- `css/tufte/` — vendored copy of [Tufte CSS](https://edwardtufte.github.io/tufte-css/) including web fonts under `css/tufte/et-book/`. **Do not modify these files**; they're upstream assets. All site pages reference `css/tufte/tufte.css` via relative paths (`../css/tufte/tufte.css` from subdirectories).
- `css/site.css` — site-wide overrides loaded *after* `tufte.css` on every page. Currently sets the global `body` font stack with Noto Serif SC as the CJK fallback for `et-book` (imported from Google Fonts via `@import`). Add other cross-page rules here rather than duplicating them inline.

### Page conventions

- Every page links `tufte.css` then `site.css` (in that order) and places content inside `<article>`.
- Navigation lists use `list-style-type: '❧ '` (a stylistic choice — keep it when adding nav-like lists).
- `projects/index.html` deviates from the default Tufte layout by overriding `body` width and removing the side-note column. `friends/index.html` uses an asymmetric variant of the same override (`margin-left` fixed, `margin-right: auto`) for an academic-journal feel.

## Working with the site

- No build / install / test. To preview locally, serve the directory with any static server (e.g. `python3 -m http.server`) and open `http://localhost:8000`.
- Deployment is automatic: pushing to `main` publishes via GitHub Pages.
- Relative paths matter — pages reference assets one level up (`../css/tufte/...`). New top-level pages should be added as a new subdirectory containing `index.html`, then linked from the root `index.html` nav list.
