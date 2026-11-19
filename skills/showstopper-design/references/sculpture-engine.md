# Parametric sculpture: the proven implementation pattern

This is a technical recipe for the approved experiment, not a required aesthetic. Use raw WebGL when real depth, material lighting, and smooth geometry matter. Use Canvas 2D when it better expresses the concept. A single HTML can embed all CSS, shaders and JavaScript without libraries or assets.

## Geometry

The working reference uses sampled tubular surfaces with indexed triangles, position/normal/UV attributes and three equally-sized geometry arrays. Its centre curves are:

- Trefoil: `((1.65 + 0.62*cos(3t))*cos(2t), (1.65 + 0.62*cos(3t))*sin(2t), 0.75*sin(3t))`.
- Orbit: `(1.8*cos(t), 1.8*sin(t), 0)` with a circular tube.
- Harmonic path: `(1.65*cos(3t), 1.5*sin(2t), 0.8*sin(5t))`.

Sample `t` from 0 to 2π inclusive. Estimate or analytically compute the tangent. Derive an orthonormal normal/binormal frame, then add `radius * (normal*cos(v) + binormal*sin(v))` around the curve. If the tangent aligns with the chosen up vector, choose a different reference vector; do not normalize a zero cross-product and silently pinch the surface. A production extension should use a parallel-transport frame for arbitrary curves.

Keep vertex counts equal when interpolating geometries. The reference uses 400 longitudinal by 48 circumferential subdivisions, producing 19,649 vertices, within a Uint16 index range. Never switch counts without validating the largest index and index-buffer type. Test performance on the target machine; these counts are not a measured frame-rate guarantee.

For a grid vertex `a=i*(V+1)+j`, `b=a+V+1`, the tested triangle winding is `(a,a+1,b)` and `(b,a+1,b+1)`. Verify winding against the supplied normals: reversing it while also flipping back-face normals in the fragment shader made the initial sculpture incorrectly dull. A normal-direction bug can look like a palette problem.

## Material and projection

Use smooth vertex normals, directional diffuse illumination, distinct specular lights and restrained Fresnel edge light. UV-based ribbing and finer cross-thread modulation create microstructure without external texture maps. The visual must have readable broad form before fine detail.

The original material uses warm-metal and pearl highlights; other designs need their own material logic. Do not make gold a default. Avoid generic rainbow shader palettes or glowing blobs behind text.

The original vertex shader rotates both positions and normals, applies a mild travelling normal displacement, and projects using camera depth and the actual viewport aspect. A click resets a narrow Gaussian pulse travelling through longitudinal UV. Tension changes surface thickness plus wave amplitude.

Keep clip-space depth inside the valid range across every pose; an overly large depth coefficient clipped the rear surface. Derive depth from actual object bounds for a new sculpture rather than copying a magic constant.

## Transformation

Use a bounded progress variable and smoothstep for a deliberate morph. Update position and normal buffers together. Renormalize interpolated normals in the shader. If the user switches again mid-transition, interpolate from the currently displayed buffers to avoid a jump.

A vertex interpolation between knot and orbit is an artistic transition, NOT a claim that a trefoil can be untied continuously without intersections. Label mathematical captions as base curves when animated surface deformations are added. Keep coefficients in the caption consistent with the implemented geometry.

## Responsive composition

Do not just shrink the desktop poster. On phone, give the object, caption, headline and controls separate vertical zones. The approved refinement moved the full caption above the sculpture and made the instruction 12px with wrapping. On desktop, keep the sculpture large while reserving the text and equation regions.

Perspective can push a rotated object outside its initial bounds. Inspect extreme poses and all three shapes at the highest deformation, not only the default. If text might collide, constrain the stage or use a dedicated text-safe region.

## Input and state

- Use pointer capture for drag; handle pointerup and pointercancel.
- Track distance so a drag does not also trigger a click burst.
- Give the canvas a descriptive accessible name, keyboard focus, and arrow-key rotation.
- Keep shape, deformation, rotation, pause, time and pulse in explicit state.
- Use a seeded PRNG for generative particle behavior.
- One pause state controls rotation, shader time, morphing and particles. Shape changes while paused still apply.
- Honour reduced motion on load and when the media query changes.
- Clamp frame delta and suspend time advancement when hidden. A hidden automation tab may throttle requestAnimationFrame; do not infer poor rendering performance from that alone.
- Keep the canvas behind content without blocking its actual hit target. Check `document.elementFromPoint()` over the sculpture and test a real drag.
- Handle unavailable WebGL with an honest static fallback; disable controls that cannot work. Keep content accessible even if rendering fails.

## Verification recipe

1. Run the inline script through Node `--check` using `subprocess.run` and script text on stdin. Do not create test output by inventing browser state.
2. Navigate to the real file or local URL with `browser_exec`; inspect the correct URL and actual viewport dimensions.
3. Check shader compile/link status and WebGL error state, then capture the visual.
4. Use real browser mouse dispatch to drag. Verify changed rotation, not only dispatched events. Exercise click, keyboard, shape switches, slider, pause and reduced motion.
5. Inspect desktop and phone screenshots, plus a visible content dialog. Check that the dialog can close via keyboard and returns focus.
6. Measure computed colour pairs by converting them to sRGB pixels in a 2D canvas before WCAG calculations. Solid-colour ratios do not settle contrast over moving highlights.
7. Confirm the served entrypoint matches the durable source bytes. Keep final screenshots tied to the current source, not earlier lighting/caption revisions.

## Tooling lessons

On Windows Bash, an interactive shim around `node` may report `stdin is not a tty`. Use `terminal` to run Python, resolve the native executable with `shutil.which('node')`, and call it through `subprocess.run(..., capture_output=True, text=True)`.

For browser JS, prefer Python triple-quoted strings and simple selectors. Avoid layers of escaped nested quotes: a malformed test expression is not an application bug. Use `querySelectorAll('[data-shape]')[1]` when that avoids ambiguous quoting.

If a browser operation unexpectedly yields an empty page, read `page_info()` and navigate to the intended URL again. Bring the actual target to the front before motion checks. Do not blindly reload a stale target.

If Hallmark's render tier lacks Puppeteer, record the limitation and use available browser tools for real visual/interaction checks. Do not install a new browser or package without permission, and do not call a static pass a rendered pass.

## Multiple modes on one stage (switcher + ES-module 3D)

When the signature grows from one object into several switchable instruments (a pendulum, a Hopf fibration, a loss surface), build a shared shell, not one giant file of tangled globals:

- **One stage host, one mode mounted at a time.** The shell owns a container element plus the shared chrome (readout panel, pause, a per-mode actions slot). Each mode is a factory returning `{id,title,mount,unmount,onKey?}` and owns its own canvas, loop, and state. Switching calls `unmount()` (cancel rAF, dispose geometry/material, remove the canvas) then `mount()`. A single canvas cannot hold both a 2D and a WebGL context, so each mode creates and removes its own canvas rather than sharing one.
- **Keep modes in their own ES-module files** imported by the stage page; pass the shell's helpers (THREE, the container, `setReadout`, `setActions`, a `paused`/`reduced` accessor) in as a context object. This keeps the page small and each instrument independently testable. It also means the page is ESM and only runs over HTTP — verify through a local server, never `file://`.
- **three.js is fine for a no-CDN self-contained site** if you vendor the module locally (`public/vendor/three.module.js`, MIT) and import it by relative path. Reuse the warm-metal `MeshStandardMaterial` and the existing tube/`TubeGeometry` so a new 3D mode stays in the same visual language instead of introducing a second renderer.
- **Bind generated controls under the slot that received them.** Markup injected by `setActions` lives in the chrome, not inside the stage container; query it under that element (or `document`), or the handlers attach to nothing and the buttons are dead.
- **Confirm each mode's numeric behaviour against a standalone simulation before baking parameters.** Tuning an optimizer or an integrator by screenshot is slow and hides sign/variable bugs — a Nesterov lookahead that reads the wrong struct field is `NaN` and never converges; a DFT whose coefficients are already in pixel units must not be re-multiplied by the stage scale. Run the loop in a few lines of Python/Node, check the step counts or error curve match the intended pedagogy, then port the exact constants.
- **Readouts update in the loop, not just on mount.** A value shown once at mount (point count, step count) goes stale while the animation runs; refresh it on a throttled tick inside the frame callback, and remember a hidden automation tab freezes that callback so the panel looks stuck until the tab is brought to front.
