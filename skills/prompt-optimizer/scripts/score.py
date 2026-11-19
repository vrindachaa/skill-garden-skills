#!/usr/bin/env python3
"""Compute PnQs v5 (agnostic) from 10 dimension values + flags.

Usage:
  python3 score.py TE COV ENF MIS MOD CLAR NOC VER TOOL FMT \\
      [--tool-required] [--tool-present] [--format-required] [--format-present] [--sys]

Order: TokenEfficiency Coverage Enforceability MisinterpretationSafety
       Modularity Clarity NoContradictions VerificationRigor
       ToolCompliance FormatCompliance

Flags:
  --tool-required    a tool/API/DSL is required by the task
  --tool-present     the prompt includes that tool usage
  --format-required  an output format/schema is required by the task
  --format-present   the prompt specifies that output format/schema
  --sys              the prompt is embedded in system instructions
"""
import argparse

DIMS = ["TokenEfficiency", "Coverage", "Enforceability",
        "MisinterpretationSafety", "Modularity", "Clarity",
        "NoContradictions", "VerificationRigor",
        "ToolCompliance", "FormatCompliance"]
WEIGHTS = [0.18, 0.14, 0.14, 0.14, 0.12, 0.10, 0.06, 0.04, 0.04, 0.04]


def band(s):
    if s == 0.0:
        return "Failing"
    if s < 1.5:
        return "Near-fail"
    if s < 3.0:
        return "Weak"
    if s < 4.0:
        return "Adequate"
    if s < 4.7:
        return "Strong"
    return "Elite"


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument('scores', nargs=10, type=float, metavar='SCORE')
    for flag in ('tool-required', 'tool-present', 'format-required', 'format-present', 'sys'):
        parser.add_argument('--' + flag, action='store_true')
    args = parser.parse_args()
    if not all(0 <= v <= 1 for v in args.scores):
        parser.error('Scores must be finite values in [0, 1].')
    d = dict(zip(DIMS, args.scores))
    tool_required, tool_present = args.tool_required, args.tool_present
    fmt_required, fmt_present = args.format_required, args.format_present
    is_sys = args.sys
    if not tool_required and not tool_present:
        d['ToolCompliance'] = 1.0
    if not fmt_required and not fmt_present:
        d['FormatCompliance'] = 1.0

    # 1. zero-floor gates
    zero = None
    for name in ["TokenEfficiency", "Coverage", "Enforceability",
                 "MisinterpretationSafety", "NoContradictions"]:
        if d[name] < 0.20:
            zero = f"{name} = {d[name]} < 0.20"
    if tool_required and not tool_present:
        zero = "ToolRequired && ToolMissing"
    if fmt_required and not fmt_present:
        zero = "FormatRequired && FormatMissing"
    if zero:
        print(f"zero-floor gate: {zero} -> 0.00")
        print("PnQs v5 final: 0.00")
        print("band: Failing")
        extremes(d)
        return

    # 2. base
    base = 5.00 * sum(d[n] * w for n, w in zip(DIMS, WEIGHTS))
    print(f"base score: {base:.2f}")

    # 3. hard caps
    cap = 5.00

    def cap_to(v, why):
        nonlocal cap
        if v < cap:
            print(f"cap -> {v:.2f} ({why})")
            cap = v

    if d["NoContradictions"] < 0.70:
        cap_to(2.00, "NoContradictions < 0.70")
    if d["Coverage"] < 0.60:
        cap_to(2.50, "Coverage < 0.60")
    if d["Enforceability"] < 0.60:
        cap_to(3.00, "Enforceability < 0.60")
    if d["MisinterpretationSafety"] < 0.60:
        cap_to(2.50, "MisinterpretationSafety < 0.60")
    if d["ToolCompliance"] < 0.60:
        cap_to(3.00, "ToolCompliance < 0.60")
    if d["FormatCompliance"] < 0.60:
        cap_to(3.00, "FormatCompliance < 0.60")
    if is_sys and d["VerificationRigor"] < 0.40:
        cap_to(3.00, "isSystemInstructions && VerificationRigor < 0.40")

    final = min(base, cap)
    print(f"cap: {cap:.2f}")
    print(f"PnQs v5 final: {final:.2f}")
    print(f"band: {band(final)}")
    extremes(d)


def extremes(d):
    hi = max(d, key=d.get)
    lo = min(d, key=d.get)
    print(f"highest scoring value: {hi}, {d[hi] * 5.00:.2f}/5.00")
    print(f"lowest scoring value: {lo}, {d[lo] * 5.00:.2f}/5.00")


if __name__ == "__main__":
    main()
