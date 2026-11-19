---
name: interactive-web-visuals
description: Build and verify interactive Canvas and Three.js visualizations.
author: V (vrindachaa), Hermes Agent
license: MIT
metadata:
  published: true
---

# Interactive Web Visuals

Build interactive mathematical / physical / data visualizations as self-contained
HTML with Canvas2D and three.js — a multi-mode "stage" the visitor manipulates, not a
video or a gallery. For one-off generative sketches reach for `p5js`; for high-impact
marketing pages, `showstopper-design`. This skill is for an instrument: drag it, read
live invariants off it, switch what it shows.

## When to use

- A page whose point is a thing you can grab, drag, and read values off (a physics
  sim, a 3D object, a function painted over a plane, an optimizer on a surface).
- Several related visuals behind one switcher ("multi-mode exhibit" with N modes).
- Any three.js / WebGL / Canvas2D interactive embedded in a site.

## Architecture: one stage, modes as modules

- **One full-viewport stage**, a `<div id="stage">` container (NOT a bare canvas). Each
  mode creates and appends its OWN canvas on mount and removes it on unmount — a single
  canvas element cannot hold both a `2d` and a `webgl` context, so mixed-renderer
  switchers must swap canvases.
- **Each mode is an object** `{ id, title, sub, formula, hint, mount, unmount, onKey?, onPause?, readouts() }`.
  A shared shell owns the chrome: the mode switcher, pause button, the readout panel,
  DPR cap, reduced-motion detection, and mount/unmount dispatch. Modes never draw their
  own chrome.
- **Put each mode in its own ES-module file** (`public/math-modes/<id>.js`) that exports
  `make<Id>(ctx)`, where `ctx = {THREE, stage, setReadout, setActions, css, api}` and
  `api` exposes `paused`/`reduced` getters. This keeps the page small and lets modes be
  built and tested one at a time. Build the shell plus ONE mode end-to-end first; add
  the rest as files once the contract holds.

## Hard pitfalls (each cost real time)

- **ES module imports are blocked over `file://`.** three.js r160+ ships ESM-only, and
  browsers refuse `import` from a `file://` page (CORS). Serve over `python -m
  http.server <port>` to develop and test; the deployed host (GitHub Pages, etc.) is
  fine. A page that worked by double-click will silently not boot once it imports a
  module. **Vendor the library locally** (`public/vendor/three.module.js`) so the site
  stays self-contained and CDN-free; verify it serves with a 200 + a sentinel string.
- **The `document.hidden` rAF trap.** In an automation or background tab,
  `requestAnimationFrame` is throttled and the standard `if (document.hidden) return;`
  loop guard early-returns forever — so the canvas never paints and a screenshot looks
  BLANK even though a real user sees it fine. Before judging any animated/canvas output
  over the browser tool: `cdp('Page.bringToFront')` and
  `cdp('Emulation.setFocusEmulationEnabled', enabled=True)` first, then PROVE it painted
  by sampling `getImageData` for a non-blank pixel or reading a live readout value —
  never trust the screenshot alone to tell you it rendered.
- **Tune numeric/algorithm params in an offline sim BEFORE baking them in.** A
  learning-rate / momentum / coefficient set that "looks plausible" can invert the
  lesson the visual exists to teach (an ill-conditioned-valley demo where plain gradient
  descent beats momentum, because the step size was unstable). Compute the outcome
  (steps-to-tolerance, convergence ordering) in a throwaway Python sim, pick params that
  give the intended result, then hardcode them. Surface non-convergence honestly — a
  capped run reads as `"400+ (capped)"`, not a bare number that looks like success.
- **Dim full-bleed bright geometry so overlay text stays legible.** When editorial text
  sits over the canvas (domain coloring, shaders, bright fields), drop brightness and
  saturation and add a scrim under the text region in-shader or in CSS. Readable text
  away from bright geometry is a hard constraint, not a nicety.
- **Resource hygiene.** Cap `devicePixelRatio` at 2 (`renderer.setPixelRatio(Math.min(devicePixelRatio,2))`);
  a fixed timestep physics loop uses a clamped accumulator so behaviour is frame-rate
  independent, with an invariant (energy drift) as a built-in correctness check; and
  `dispose()` every geometry + material + renderer on unmount or WebGL contexts leak
  across mode switches until the browser kills the oldest.

## Self-contained + accessible (standing constraints)

- No CDN, no remote fonts or images, no build step, no npm — inline CSS, vendor every
  library locally. These sites are one self-contained HTML per page by convention.
- Follow the host application’s contrast and theme requirements. Use its existing design tokens.
- Keyboard parity for every gesture (drag has an arrow-key / Tab equivalent), a designed
  reduced-motion still frame (precompute the completed trajectory, offer manual step),
  and an honest no-WebGL / no-JS fallback.

## Verify over CDP, every build (a worker's "it renders" is not proof)

1. Start `python -m http.server`; load over `http://127.0.0.1:...`, bring the tab to
   front + enable focus emulation (the `document.hidden` trap above).
2. Cycle EVERY mode: confirm it mounts (`#stage canvas` present), answers pointer AND
   keyboard, and its readouts populate. Screenshot each; inspect with your own vision.
3. Overflow sweep at 320 / 390 / 1280 / 1440 px on every mode — `document.documentElement.scrollWidth > innerWidth` must be false.
4. Broken-link check: resolve every local `href`/`src` to an on-disk file.
5. For physics/algorithm modes, assert the invariant and the intended ordering from the
   live readouts (energy drift < threshold; optimizer A fewer steps than B), not from
   how it looks.

## Verification checklist

- Serves and boots over HTTP (modules load); vendored library returns 200.
- Every mode mounts, responds to drag + keyboard, unmounts cleanly (no context leak).
- No horizontal overflow at 320/390/1280/1440; no broken local links.
- Overlay text readable over the brightest frame of every mode.
- Reduced-motion and no-WebGL paths produce useful content.
