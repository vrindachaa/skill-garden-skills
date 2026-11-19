---
name: gallerize
description: Design a browsable visual world for a real collection.
author: V (vrindachaa), Hermes Agent
license: MIT
metadata:
  published: true
---

# Gallerize

Use when a list of real objects should become a place to explore. A coat of paint on a card grid is not a representation.

1. Inspect the named material. Record item IDs, grouping, provenance, measured quantities, and sourced relationships. Keep uncertainty; don't invent connections for a prettier picture.
2. Write three proposals in this form: “The items become ___; related items ___; visitors discover a connection by ___.” Change the material, spatial logic and gesture, not just the color. Use `python scripts/concept_brief.py manifest.json` for a first pass, not as the final art direction. Ask for a choice before building the collection.
3. Write the approved contract from `references/representation-contract.md`. Make one small scene at viewing size and one close-up; the scene should read even with labels and glow off. When feedback is vague, ask which silhouette, material or camera angle to keep.
4. Implement the approved scene. For a bed-based garden only, `python scripts/gallerize_beds.py manifest.json -o garden.html` gives a standalone starting point. See `references/botanical-scene.md` and `references/flower-morphology.md`. For another representation build the appropriate scene rather than renaming beds. Use only trusted input manifests; review any embedded full text before distributing the HTML.
5. Let the visitor inspect one object and travel along a real edge. Show units for quantitative encodings. Keep keyboard selection independent of animation, make the dossier dismissible, and offer a static alternative to motion.
6. Exercise all items on desktop and a narrow viewport; inspect screenshots at rest and on selection. Check totals and edges against the manifest, check focus and overflow, then deliver the artifact with its regeneration command and limitations.
