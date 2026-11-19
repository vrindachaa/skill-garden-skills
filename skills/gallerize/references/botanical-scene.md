# Botanical scene recipe

Use when the approved representation maps collection items to plants. The garden must be the picture, not a UI with plant icons attached.

## Composition

- Put the entities in the scene itself. For bed-based references, use one horizontal soil bed per category, stacked vertically, each with its own soil strip and label; root every stem in that bed's baseline. Sort beds by item count so the largest beds appear first and at least two beds are visible in a desktop first viewport. A row of flower heads with no visible stems reads as floating icons.
- Give the subject the majority of the first viewport. Title, search, and filters belong in the corners as small overlays; a large header block plus a strip of plants is a dashboard, not a garden.
- Keep chrome out of the subject zone. Bottom-mounted search/filter bars cover plant labels; put controls in a top corner and leave the ground area clear.
- Make each entity visually substantial: layered two-tone petals, a lighter inner highlight, a darker edge stroke, and a textured center. Six flat one-color petal shapes do not survive a close look.
- Derive distinct flower morphologies (peony, rose, daisy, tulip, spike, bell, cluster) and bind the primary species to the bed/category so each bed reads as a species stand. Vary stem height, bloom scale, and color within the bed from real numeric attributes; do not vary only color.

## SVG geometry

- Pick a `viewBox` whose aspect ratio is close to the target viewport, then use `preserveAspectRatio="xMidYMid meet"` so the whole scene fits. A tall viewBox with `slice` crops the top in a short viewport and leaves back-row flower heads floating without stems.
- Verify geometry in the browser, not in source: read each plant's `getBoundingClientRect().top/bottom` against `innerHeight`, and confirm no horizontal overflow.
- Root stems in their bed's soil baseline; when a bed has depth rows, keep those rows near the same baseline with small offsets. Large vertical gaps between rows break the shared-ground illusion.
- Space entities so their rendered width at their scale is <= their horizontal spacing. In a 1600px-wide scene, 15 items per row means ~100px spacing; a 150px-wide plant at scale 1 will collide.
- Truncate on-scene labels to about 16 characters and put the full name in the detail view. Long skill names otherwise render into each other as one unreadable string.
- Draw vines from the same coordinate function that places the plants, using the persisted relationship graph. Decorative edges that do not correspond to manifest relationships are a factual error.

## Height encoding

- Read real source measurements for numeric encodings. For skill gardens, count lines in each `SKILL.md`, store both `lines` and a normalized `size`, then compute SVG `viewBox` height and plant pixel height from that value.
- Normalize against the actual range in the collection, not a guessed maximum. Verify minimum and maximum rendered plant heights in the browser; a range that is too narrow makes the encoding invisible.
- When flower heads read oversized, scale only the bloom group around its center. Do not scale the whole plant: that shortens the stem and destroys the height signal.

## Detail view and full source

- Use a slide-in specimen dossier, not a generic centered modal: enlarged flower hero, bed/species/status line, real stats, sourced relationships, and a full-source toggle.
- Embed full source text in the manifest when the gallery must stay offline. Escape `</` as `<\/` in the JSON payload before injecting it into a `<script>` tag.
- Close the panel by button, overlay click, and Escape, and return focus to the originating plant where practical.

## Three.js scene and dense beds

- Keep `manifest.json` as the single source of truth. In Three.js: bed = planter group, plant = mesh group, stem height = normalized line count, species = geometry variant, relationship = edge.
- Start at grass height facing the beds, with a dawn gradient sky, warm hemisphere light, and instanced grass around the planters; a high camera over bare ground reads as beds in space.
- Use one uniform bed width for all categories. Collapse single-item categories into a related bed, but keep `nativeBed`, `family`, and `species` on the item and show them in the specimen panel so provenance survives the merge.
- Add a transparent raycast hitbox around each bloom. On hover, scale the bloom, brighten its additive halo, show a pointer cursor, and display a small `name · lines` tooltip; a clickable object without a hover affordance feels dead.
- Keep default halo opacity and petal emissive at 0; on hover lerp halo to ~0.48 and emissive to ~0.22. Store petal materials on the head group so the animation loop updates them without traversing the whole scene.
- Build 3D petals by sweeping an arc cross-section along a center-vein curve — see `references/flower-morphology.md` for the formula, the sharpened-cusp waveform, and sourced per-species structure. A flat extruded shape with a parabolic cup offset reads as a disk; scaled spheres read as cartoon balloons. Apply slight HSL, rotation and scale jitter per petal. Cache geometry in a `Map` keyed by the full parameter set — generating a fresh geometry per petal stalls page load in dense gardens. When a 2D SVG scene uses `ExtrudeGeometry`, call `computeBoundingBox()` and remap its UVs into 0–1 from the bounding box; default `ExtrudeGeometry` UVs are in shape units and otherwise sample only one corner of a texture. For each base color, cache a small canvas texture with a base-to-light gradient, faint vein strokes, a soft highlight, and margin shading on both lateral edges so overlapping petals stay delineated; assign it as `map` with `color: 0xffffff` and keep `emissiveIntensity` at 0 until hover.
- Reduce ambient/hemisphere intensity enough that the directional light shapes the petals. Flat ambient light makes even organic geometry look flat and toy-like.
- Use two centered depth rows inside each planter for dense beds: `perRow = ceil(n / 2)`, back row at `z - 1.45`, front row at `z + 1.45`; keep planter width uniform and depth ~6, and expand the grass-exclusion half-depth to cover the deeper planter.
- Vendor `three.module.js` locally (copy from a licensed local vendor directory) and serve over HTTP (`python -m http.server 8765 --directory <project>`); ES modules fail from `file://`.
- Deliver a named project folder with `index.html`, `manifest.json`, `generate.py`, `preview.png`, `README.md`, and the original reference images, plus the `three/` subfolder for the 3D port.

## Verification

- Capture the resting frame with every overlay closed; a screenshot of the detail panel cannot establish how the garden looks.
- Before trusting a close-up audit, project entity world positions to screen coordinates and confirm the intended entity is near center; an audit of a mis-framed capture describes the wrong flower with full confidence.
- Build a large front-and-side proof sheet of candidate species and get it approved before applying a petal direction across the whole collection.
- Inspect the capture and answer concretely: are all entities rooted with visible stems, do shapes and heights vary, is the subject dominant, are labels legible and non-overlapping, does the whole scene fit?
- Confirm entity count, edge count, label sample, viewBox, and overflow numerically in the browser before reporting.
- Ship a stdlib `unittest` suite that checks item count, collapsed-bed provenance, real metrics/full source presence, generator reproducibility, local vendor module, and artifact contracts. Scope external-resource assertions to the `<head>`; embedded SKILL.md text legitimately contains URLs and `<script src=` examples.
