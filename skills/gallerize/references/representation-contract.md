# Representation contract

A representation is not a theme. It is the rule that turns collection data into a visual world.

## Required fields in a manifest

```json
"representation": {
  "type": "bed-garden",
  "world": "dawn garden seen from grass level",
  "entity": "flowering plant",
  "encodings": {
    "group": "bed + flower species",
    "size": "stem height from real line count",
    "lifecycle": "seed / sprout / bloom",
    "relations": "clickable dossier links"
  },
  "spatial_logic": "one bed per group, two centered rows, uniform bed width",
  "interaction": "orbit, hover-to-reveal, inspect, read full source",
  "provenance": "nativeBed/family/species retained when groups are merged"
}
```

## Rules

- Every encoding must name a real field in the manifest. No decorative metrics.
- If groups are merged, keep provenance on the item and show it in the detail view.
- If the user supplied references, describe the visual grammar in `spatial_logic`; do not just name a palette.
- Concepts must differ in entity, spatial logic, interaction and narrative. Three palettes are not three concepts.
- The built-in renderers are examples, not defaults. A new collection gets a new approved contract before rendering.
- The renderer must reject a manifest with no representation instead of choosing one.

## Concept brief workflow

1. Run `python scripts/concept_brief.py manifest.json` for three starting directions.
2. Read the real source and references, then rewrite the briefs in domain-specific language.
3. Present them to the user and require a choice.
4. Copy the approved brief into the manifest's `representation` object, adding exact field mappings.
5. Only then build or adapt a scene.
