# Flower morphology and the petal engine

For botanical representations where the flowers must survive a close look. Sourced facts first, then the geometry that renders them.

## Petal engine: sweep a cross-section along a center vein

The standard interactive-flower-modeling approach (Ijiri et al., *Floral diagrams and inflorescences*) builds a petal by transforming a cross-section along a **center vein**. Reproduce that; do not bend a flat sheet.

Two independent curvatures are what make a petal read as volume:

1. **Lengthwise** — the vein curve supplies rise, flare, and tip reflex.
2. **Across the width** — a true circular arc supplies cupping.

Per species define `out(t)`, `up(t)`, `width(t)`, `cup(t)` for `t` in 0..1 along the petal, then build a `(NV x NU)` grid:

```js
// vein point and frame
T = normalize(dP/dt)              // tangent in the radial-vertical plane
N = (0, T.z, -T.y)                // surface normal, lifts toward +y
// circular-arc cross-section, half-angle a = cup(t), half-width w = width(t)
R   = w / sin(a)
lat = R * sin(a * u)              // u in -1..1, lateral offset
dep = R * (cos(a * u) - cos(a))   // bulge along N
vertex = P + (lat, 0, 0) + N * dep
```

A parabolic `cup * (1 - u*u)` offset on a flat extrusion is the failure mode: it has one shallow curvature and renders as a disk under any lighting.

- `cup(t)` decreasing along the petal opens the tip; increasing it tightens a furled center.
- Posture belongs in the vein. With rise and reflex baked into `up(t)`, mounting is only `rotation.y = azimuth`, a radial offset, and a small roll. Mount-pitch hacks tip whole whorls the wrong way.
- Margin ripples: add to `dep` an edge-weighted term `pow(abs(u), ~2.6) * wave(cusps * PI * u) * pow(t, ~1.25)`.
- Sharp cusps need a sharpened waveform — `sign(s) * pow(abs(s), 0.55)` — not a plain sine, which gives soft carnation-style ruffles instead.
- Cache geometry in a `Map` keyed by the full parameter set, and cache **materials** by their option key too; per-petal geometry generation stalls dense scenes, and a fresh material per petal across dozens of entities multiplies draw-call state changes for textures that are already shared.

## Petal material

- Gradient base-to-tip canvas texture, faint vein strokes, one soft diagonal highlight.
- **End the gradient at a slightly lightened tip colour, not pure white.** A ramp that terminates in white drains the hue once the entity is small on screen, so a saturated species renders as cream and the palette encoding silently stops carrying meaning. Keep the white highlight veil weak (~0.1 alpha) and filmic tone-mapping exposure near 1.0; push the base colour deeper rather than brightening the scene.
- **Margin shading on both lateral edges** so overlapping same-colored petals stay delineated; without it a whorl fuses into one mass.
- Radial alpha map fading toward the outline so silhouettes dissolve into a dark scene instead of cutting out.
- Optional dark basal blotch for species that have one.
- Keep `emissiveIntensity` at 0 by default; lift on hover only.

## Sourced species facts

| Species | Structure to honour |
|---|---|
| **Rose** | Petals form a cupped surface with **sharp cusps**, from MCP (Mainardi-Codazzi-Peterson) incompatibility — not the smooth wavy edge that Gauss incompatibility gives a carnation. Older/outer petals develop **more cusps**; the surface goes saddle-like near a cusp. Arrange on the **golden angle** (~137.5 deg), with cupping tightening inward, cusp count falling inward, and outer petals reflexing at the tip. |
| **Poppy** (*Papaver rhoeas*) | **Four** broadly ovate petals, crinkled like tissue paper, slightly overlapping, usually with a **dark blotch at the base**. Numerous stamens with **blue-black anthers on slender dark filaments**; stigma is a **disk with 8-12 rays**. Two sepals drop as the flower opens. |
| **Lily** | Six tepals that spread outward and slightly **up**, with the tips rolling back. Prominent pistil plus six stamens on curving filaments with large anthers. Drooping petals are the classic mount-angle bug, not a lily. |
| **Lily of the valley** | Small **nodding bells** on short curved pedicels along an arching stem, six recurved lobes at each rim, tiny pale stamens inside, one broad lanceolate leaf. Build the bell as a lathe body plus individually recurved lobes. |
| **Cosmos** | Eight spatulate ray florets around a granular central disk; the face is **flat and open**, gently dished at most. Petals folding inward is a bug. |
| **Peony** | Nested whorls; the **outer whorls lie nearly flat** and inner whorls stand progressively upright. Uniformly upright rings read as a closed bud. |
| **Iris** | Three **falls** that arc out then hang down, each with a fuzzy **beard**, plus three **standards** that stand up and arch inward. |

Phyllotaxis note: spiral arrangements use a constant divergence angle (golden angle for the common case), which is why ray-floret and petal counts cluster on Fibonacci numbers. Use it for spiral species instead of evenly-spaced rings.

## Lighting for organic geometry

Keep ambient and hemisphere light low enough that a directional key light shapes the petals, add a cool rim light and a weak under-light, and use filmic tone mapping. Flat ambient light makes even correct geometry look like a toy.
