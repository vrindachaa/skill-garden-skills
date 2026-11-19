#!/usr/bin/env python3
"""Training gradebook — durable record of what was taught and what stuck.

Store: training/gradebook.json  (override with --root)
stdlib only. Atomic writes. Never hand-edit the JSON.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

DEFAULT_ROOT = Path("training")

EVENTS = (
    "placement", "enrolled", "signoff", "baseline", "formative", "attempt",
    "eval", "retention", "graduated", "escalated", "rubric-fault", "withdrawn",
)
# Events whose letter grades count toward the attempt GPA.
GRADED_EVENTS = ("baseline", "attempt", "eval", "retention")
GRADES = ("A", "B", "C", "F", "I")  # I = incomplete (harness error): not a grade, not an attempt
POINTS = {"A": 4.0, "B": 3.0, "C": 2.0, "F": 0.0}


def now() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def gb_path(root: Path) -> Path:
    return root / "gradebook.json"


def load(root: Path) -> dict:
    p = gb_path(root)
    if not p.exists():
        return {"version": 1, "created": now(), "events": []}
    return json.loads(p.read_text(encoding="utf-8"))


def save(root: Path, data: dict) -> None:
    root.mkdir(parents=True, exist_ok=True)
    p = gb_path(root)
    tmp = p.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    os.replace(tmp, p)


def cmd_init(a) -> int:
    root = Path(a.root)
    data = load(root)
    (root / "courses").mkdir(parents=True, exist_ok=True)
    save(root, data)
    print(f"gradebook ready: {gb_path(root)} ({len(data['events'])} events)")
    return 0


def cmd_record(a) -> int:
    root = Path(a.root)
    if a.event not in EVENTS:
        print(f"error: --event must be one of {', '.join(EVENTS)}")
        return 2
    if a.grade and a.grade not in GRADES:
        print(f"error: --grade must be one of {', '.join(GRADES)}")
        return 2
    if a.event == "attempt" and not (a.exam and a.attempt and a.grade):
        print("error: event=attempt requires --exam, --attempt and --grade")
        return 2
    if a.event == "graduated" and not (a.skill and a.grade):
        print("error: event=graduated requires --skill and --grade (the final course letter)")
        return 2
    if a.event == "graduated" and a.grade not in ("A", "B", "C"):
        print("error: a student cannot graduate with an F or I — record 'escalated' instead")
        return 2

    data = load(root)
    ev = {
        "ts": now(),
        "student": a.student,
        "course": a.course,
        "event": a.event,
    }
    for k in ("exam", "attempt", "grade", "self_grade", "skill", "notes",
              "attribution", "evidence", "entrustment"):
        v = getattr(a, k, None)
        if v not in (None, ""):
            ev[k] = v
    if a.cost is not None:
        ev["cost_usd"] = a.cost
    if a.calibration is not None:
        ev["calibration_gap"] = a.calibration
    elif a.self_grade and a.grade and a.grade in POINTS and a.self_grade in POINTS:
        ev["calibration_gap"] = round(POINTS[a.self_grade] - POINTS[a.grade], 2)
    data["events"].append(ev)
    save(root, data)
    print(f"recorded: {a.student} / {a.course} / {a.event}" + (f" / {a.grade}" if a.grade else ""))
    return 0


def _by_student(data: dict) -> dict:
    out: dict[str, list] = {}
    for ev in data["events"]:
        out.setdefault(ev["student"], []).append(ev)
    return out


def cmd_show(a) -> int:
    data = load(Path(a.root))
    groups = _by_student(data)
    targets = [a.student] if a.student else sorted(groups)
    if not targets:
        print("gradebook is empty")
        return 0
    for s in targets:
        evs = groups.get(s, [])
        print(f"\n=== {s} ({len(evs)} events) ===")
        spend = sum(e.get("cost_usd", 0) or 0 for e in evs)
        for e in evs:
            bits = [e["ts"], e["event"]]
            for k in ("course", "exam", "attempt", "grade", "self_grade",
                      "calibration_gap", "entrustment", "skill", "attribution"):
                if e.get(k) not in (None, ""):
                    bits.append(f"{k}={e[k]}")
            line = "  " + "  ".join(str(b) for b in bits)
            if e.get("notes"):
                line += f"\n      {e['notes']}"
            print(line)
        if spend:
            print(f"  -- recorded spend: ${round(spend, 4)}")
        gpa = _gpa([e.get("grade") for e in evs if e["event"] in GRADED_EVENTS])
        if gpa is not None:
            print(f"  -- attempt GPA: {gpa:.2f} ({_letter(gpa)})")
    return 0


def _gpa(grades) -> float | None:
    pts = [POINTS[g] for g in grades if g in POINTS]
    return sum(pts) / len(pts) if pts else None


def _letter(gpa: float) -> str:
    return "A" if gpa >= 3.5 else "B" if gpa >= 2.5 else "C" if gpa >= 1.5 else "F"


def active_graduations(events):
    active = {}
    for event in events:
        skill = event.get("skill")
        if event["event"] == "graduated" and skill:
            active[skill] = event
        elif event["event"] == "withdrawn":
            active.pop(skill, None)
    return list(active.values())


def cmd_transcript(a) -> int:
    """What a student provably knows: graduated skills only."""
    data = load(Path(a.root))
    groups = _by_student(data)
    targets = [a.student] if a.student else sorted(groups)
    for s in targets:
        grads = [e for e in groups.get(s, []) if e["event"] == "graduated"]
        active_grads = active_graduations(groups.get(s, []))
        print(f"\n=== transcript: {s} ===")
        if not active_grads:
            print("  no graduated skills — nothing provably learned")
        for e in active_grads:
            print(f"  {e.get('skill')}  grade={e.get('grade', '?')}  (course={e.get('course')}, {e['ts'][:10]})"
                  + (f"  — {e['notes']}" if e.get("notes") else ""))
        open_courses = sorted({e.get("course") for e in groups.get(s, [])
                               if e["event"] in ("enrolled", "signoff")}
                              - {e.get("course") for e in grads}
                              - {e.get("course") for e in groups.get(s, []) if e["event"] in ("escalated", "withdrawn")})
        for c in open_courses:
            if c:
                print(f"  [in progress] {c}")
    return 0


def cmd_render(a) -> int:
    root = Path(a.root)
    data = load(root)
    groups = _by_student(data)
    lines = ["# Gradebook", "", f"_regenerated {now()} — do not hand-edit; see gradebook.json_", ""]
    if not groups:
        lines.append("No training recorded yet.")
    for s in sorted(groups):
        evs = groups[s]
        grads = active_graduations(evs)
        esc = [e for e in evs if e["event"] == "escalated"]
        spend = round(sum(e.get("cost_usd", 0) or 0 for e in evs), 4)
        gpa = _gpa([e.get("grade") for e in evs if e["event"] in GRADED_EVENTS])
        gaps = [e["calibration_gap"] for e in evs if isinstance(e.get("calibration_gap"), (int, float))]
        ent_parts = [f"{e.get('skill', '?')}=L{e['entrustment']}" for e in grads if e.get("entrustment")]
        lines += [f"## {s}", "",
                  f"- graduated skills: {', '.join(e.get('skill', '?') for e in grads) or 'none'}",
                  f"- graded GPA: {format(gpa, '.2f') if gpa is not None else 'n/a'}"
                  + (f" ({_letter(gpa)})" if gpa is not None else ""),
                  f"- mean calibration gap: {round(sum(gaps)/len(gaps), 2) if gaps else 'n/a'}"
                  + (" (positive = overconfident)" if gaps else ""),
                  f"- entrustment: {', '.join(ent_parts) or 'n/a'}",
                  f"- escalations: {len(esc)}",
                  f"- recorded spend: ${spend}", "",
                  "| when | event | course | exam | attempt | grade | notes |",
                  "|---|---|---|---|---|---|---|"]
        for e in evs:
            lines.append("| {} | {} | {} | {} | {} | {} | {} |".format(
                e["ts"][:16], e["event"], e.get("course", ""), e.get("exam", ""),
                e.get("attempt", ""), e.get("grade", e.get("skill", "")),
                (e.get("notes", "") or "").replace("|", "/").replace("\n", " ")))
        lines.append("")
    out = root / "GRADEBOOK.md"
    root.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Training gradebook")
    ap.add_argument("--root", default=str(DEFAULT_ROOT))
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init").set_defaults(fn=cmd_init)

    r = sub.add_parser("record")
    r.add_argument("--student", required=True)
    r.add_argument("--course", required=True)
    r.add_argument("--event", required=True, choices=EVENTS)
    r.add_argument("--exam")
    r.add_argument("--attempt")
    r.add_argument("--grade", choices=GRADES, help="A/B/C/F, or I for a harness-error run")
    r.add_argument("--skill")
    r.add_argument("--self-grade", choices=GRADES, help="the student's own grade — feeds calibration gap")
    r.add_argument("--calibration", type=float,
                   help="override the computed gap (points, self minus actual)")
    r.add_argument("--entrustment", type=int, choices=(1, 2, 3, 4, 5),
                   help="supervision level at graduation (ten Cate)")
    r.add_argument("--attribution", choices=("student", "lesson", "rubric", "subject"),
                   help="for escalated/rubric-fault: whose fault, honestly")
    r.add_argument("--evidence", help="path to the course/attempt folder")
    r.add_argument("--notes")
    r.add_argument("--cost", type=float, help="reported USD estimate from the attempt's usage.json")
    r.set_defaults(fn=cmd_record)

    s = sub.add_parser("show")
    s.add_argument("--student")
    s.set_defaults(fn=cmd_show)

    t = sub.add_parser("transcript")
    t.add_argument("--student")
    t.set_defaults(fn=cmd_transcript)

    sub.add_parser("render").set_defaults(fn=cmd_render)

    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
