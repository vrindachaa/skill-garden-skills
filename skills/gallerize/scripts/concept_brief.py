#!/usr/bin/env python3
"""Generate three starting concept briefs from a collection manifest.

This is a thinking aid, not an art director. Always refine the output against the
real source and the user's references before presenting it.

Usage: python concept_brief.py manifest.json
"""
import argparse, json
from pathlib import Path


def signals(m):
    items = m.get('items', [])
    keys = set()
    for it in items:
        keys.update(it.keys())
        keys.update((it.get('meta') or {}).keys())
    return {
        'count': len(items),
        'has_stage': bool(keys & {'stage', 'status', 'lifecycle', 'maturity'}),
        'has_size': bool(keys & {'size', 'lines', 'length', 'weight', 'duration'}),
        'has_relations': bool(m.get('relationships') or any(
            it.get('relationships') or it.get('links') for it in items)),
        'has_group': bool(keys & {'bed', 'category', 'family', 'group', 'type'}),
        'has_time': bool(keys & {'date', 'created', 'updated', 'year'}),
        'has_tension': bool(keys & {'question', 'open_question', 'tension', 'unresolved'}),
    }


def briefs(m):
    s = signals(m)
    title = m.get('title', 'Collection')
    out = []
    out.append({
        'name': 'Living Atlas',
        'world': 'a cultivated landscape read from ground level',
        'entity': 'plants whose species, height and color carry data',
        'spatial_logic': 'separate beds per group, two centered rows per bed',
        'interaction': 'orbit, hover to reveal identity, click to inspect a specimen dossier',
        'encodings': {'group': 'bed', 'size': 'stem height', 'family': 'flower species'},
        'fit': 'Strong when the collection has categories and a real magnitude field.' if s['has_group'] and s['has_size'] else 'Use only if categories and magnitude can be sourced honestly.',
    })
    out.append({
        'name': 'Field Notes',
        'world': 'a working surface of pinned scraps and marginalia',
        'entity': 'notes whose condition encodes certainty',
        'spatial_logic': 'clusters by theme, overlap by relationship',
        'interaction': 'pull a note forward to read it, follow cross-references',
        'encodings': {'tension': 'torn edge / ink', 'group': 'pin color', 'relations': 'thread lines'},
        'fit': 'Strong when items carry open questions, drafts or unresolved states.' if s['has_tension'] else 'Weaker here unless unresolved states exist in the source.',
    })
    out.append({
        'name': 'Night Constellation',
        'world': 'a dark sky with objects at different distances',
        'entity': 'stars whose brightness and orbit encode maturity and relation',
        'spatial_logic': 'clusters become constellations, outliers remain isolated',
        'interaction': 'fly to a star, trace its connections, focus one object at a time',
        'encodings': {'size': 'brightness', 'relations': 'constellation lines', 'time': 'trail length'},
        'fit': 'Strong when relationships or time are the most interesting signal.' if s['has_relations'] or s['has_time'] else 'Weaker here unless relations or time are real fields.',
    })
    return {'title': title, 'signals': s, 'concepts': out}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('manifest')
    a = ap.parse_args()
    m = json.loads(Path(a.manifest).read_text(encoding='utf8'))
    print(json.dumps(briefs(m), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
