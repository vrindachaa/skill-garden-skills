#!/usr/bin/env python3
"""Run one exam attempt against a student Hermes profile.

Invokes `hermes -p <student> -z "<prompt>"` one-shot, captures stdout/stderr/usage,
and writes everything under <course>/attempts/<exam>/attempt-<n>/.

Preflight refusals never start the student. Ambiguous runtime failures require
evidence review before a retry; a timeout is not proof of no model work.

stdlib only.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path


def find_hermes() -> str | None:
    # Never send prompt text through a command-shell batch wrapper on Windows.
    return shutil.which("hermes.exe" if os.name == "nt" else "hermes")


def profile_exists(hermes: str, student: str) -> bool:
    try:
        out = subprocess.run([hermes, "profile", "list"], capture_output=True,
                             encoding="utf-8", errors="replace", timeout=60, check=True).stdout
    except (OSError, subprocess.SubprocessError):
        return False
    return any(row.strip().lstrip("◆* ").split()[:1] == [student] for row in out.splitlines())


def main() -> int:
    ap = argparse.ArgumentParser(description="Run one student exam attempt.")
    ap.add_argument("--student", required=True, help="student Hermes profile name")
    ap.add_argument("--course", required=True, help="course folder (absolute)")
    ap.add_argument("--exam", required=True, help="exam id, e.g. 01-blockout")
    ap.add_argument("--attempt", required=True, choices=("0-baseline", "formative-1", "formative-2", "1", "2", "3"))
    ap.add_argument("--prompt-file", help="path to the exam prompt (relative to --course or absolute)")
    ap.add_argument("--prompt", help="inline prompt text (use --prompt-file normally)")
    ap.add_argument("--timeout", type=int, default=900, help="seconds (default 900)")
    ap.add_argument("--cwd", help="working directory for the student run")
    ap.add_argument("--model", help="model override for the student run")
    ap.add_argument("--reasoning", help="reasoning level override")
    ap.add_argument("--extra", nargs=argparse.REMAINDER,
                    help="extra args passed through to hermes, after --")
    args = ap.parse_args()

    if not all(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", value) for value in (args.exam, args.student)):
        ap.error("student and exam must be plain identifiers")
    course = Path(args.course).resolve()
    if not course.is_dir():
        print(f"HARNESS-ERROR: course folder not found: {course}")
        return 2

    signoff = course / ("PLACEMENT-APPROVAL.md" if args.attempt == "0-baseline" else "SIGNOFF.md")
    if not signoff.is_file() or not signoff.read_text(encoding="utf-8").strip():
        print(f"REFUSED: written authorization missing: {signoff.name}")
        return 3

    if args.prompt_file:
        pf = Path(args.prompt_file)
        if not pf.is_absolute():
            pf = course / args.prompt_file
        if not pf.exists():
            print(f"HARNESS-ERROR: prompt file not found: {pf}")
            return 2
        prompt = pf.read_text(encoding="utf-8")
        prompt_src = str(pf)
    elif args.prompt:
        prompt = args.prompt
        prompt_src = "<inline>"
    else:
        print("HARNESS-ERROR: one of --prompt-file / --prompt is required")
        return 2

    if not prompt.strip():
        print("HARNESS-ERROR: prompt is empty")
        return 2

    hermes = find_hermes()
    if not hermes:
        print("HARNESS-ERROR: `hermes` executable not found on PATH")
        return 2

    if not profile_exists(hermes, args.student):
        print(f"HARNESS-ERROR: profile '{args.student}' not in `hermes profile list`")
        return 2

    outdir = course / "attempts" / args.exam / f"attempt-{args.attempt}"
    try:
        outdir.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        print("REFUSED: attempt directory already exists; preserve previous evidence")
        return 3
    usage_path = outdir / "usage.json"

    cmd = [hermes, "-p", args.student]
    if args.model:
        cmd += ["-m", args.model]
    if args.reasoning:
        cmd += ["--reasoning", args.reasoning]
    cmd += ["-z", prompt, "--usage-file", str(usage_path)]
    if args.extra:
        cmd += [a for a in args.extra if a != "--"]

    (outdir / "prompt.txt").write_text(prompt, encoding="utf-8")

    env = dict(os.environ)

    start = time.time()
    timed_out = False
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=args.timeout, cwd=args.cwd or None, env=env,
        )
        stdout, stderr, rc = proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired as e:
        timed_out = True
        stdout = (e.stdout or b"").decode("utf-8", "replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        stderr = (e.stderr or b"").decode("utf-8", "replace") if isinstance(e.stderr, bytes) else (e.stderr or "")
        rc = -1
    duration = round(time.time() - start, 1)

    (outdir / "stdout.txt").write_text(stdout or "", encoding="utf-8")
    (outdir / "stderr.txt").write_text(stderr or "", encoding="utf-8")

    usage: dict = {}
    if usage_path.exists():
        try:
            parsed = json.loads(usage_path.read_text(encoding="utf-8"))
            usage = parsed if isinstance(parsed, dict) else {"_parse_error": True}
        except (OSError, ValueError):
            usage = {"_parse_error": True}

    # Harness vs student classification.
    harness_error = None
    if timed_out:
        harness_error = f"timeout after {args.timeout}s"
    elif rc != 0:
        harness_error = f"exit {rc}"
    elif not (stdout or "").strip():
        harness_error = "empty stdout (model produced no final response)"

    meta = {
        "student": args.student,
        "exam": args.exam,
        "attempt": args.attempt,
        "course": str(course),
        "prompt_source": prompt_src,
        "command": [hermes, "-p", args.student, "-z", "<prompt>", "--usage-file", str(usage_path)],
        "cwd": args.cwd or os.getcwd(),
        "exit_code": rc,
        "duration_s": duration,
        "timed_out": timed_out,
        "stdout_chars": len(stdout or ""),
        "classification": "needs-review" if harness_error else "gradeable",
        "review_reason": harness_error,
        "usage": usage,
        "counts_as_attempt": None if harness_error else args.attempt in ("1", "2", "3"),
    }
    (outdir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    cost = next((v for v in (usage.get("estimated_cost_usd"),
                (usage.get("total_including_auxiliary") or {}).get("estimated_cost_usd"),
                usage.get("estimated_cost"), usage.get("cost"), usage.get("total_cost")) if v is not None), None)
    cost_s = f"${cost}" if cost is not None else "cost=unknown"
    if harness_error:
        print(f"NEEDS-REVIEW ({harness_error}) — inspect usage and artifacts before retrying. {duration}s, {cost_s}")
        print(f"evidence: {outdir}")
        return 4

    print(f"GRADEABLE: exit {rc}, {duration}s, {len(stdout)} chars, {cost_s}")
    print(f"evidence: {outdir}")
    print(f"next: grade against rubrics/{args.exam}.md and write {outdir / 'GRADE.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
