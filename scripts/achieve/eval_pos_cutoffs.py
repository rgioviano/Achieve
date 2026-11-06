#!/usr/bin/env python3
"""Classify Achieve eval ROM screens as Pos / Neg from locked cutoffs.

House rules (Ryne 2026-11-03) + PRI manual degree cutoffs.
No network. Python 3 stdlib only.

Examples
  python3 eval_pos_cutoffs.py --fa-ir-r 40 --fa-ir-l 50 --fa-er-r 55 --fa-er-l 45
  python3 eval_pos_cutoffs.py --json '{"fa_ir":{"r":40,"l":50},"hg_er":{"r":85,"l":95}}'
  python3 eval_pos_cutoffs.py --list
  echo '{"slr":{"r":70,"l":110},"shoulder_flexion":{"r":150,"l":170}}' | python3 eval_pos_cutoffs.py --stdin

Exit 0 always when input parses; exit 2 on bad args.
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

# Locked + PRI degree rules. Soft HG IR band noted in skill.
CUTOFFS: dict[str, dict[str, Any]] = {
    "fa_ir": {
        "label": "FA IR",
        "kind": "lt",
        "threshold": 45,
        "source": "Ryne locked 2026-11-03",
        "asana": "FA IR",
    },
    "fa_er": {
        "label": "FA ER",
        "kind": "lt",
        "threshold": 50,
        "source": "Ryne locked 2026-11-03",
        "asana": "FA ER",
    },
    "hg_er": {
        "label": "HG ER",
        "kind": "lt",
        "threshold": 90,
        "source": "Ryne locked 2026-11-03",
        "asana": "HG ER",
    },
    "hg_ir": {
        "label": "HG IR",
        "kind": "lt",
        "threshold": 85,
        "soft_low": 80,
        "soft_high": 90,
        "source": "PRI Postural Respiration (<80-90°); house midpoint 85°",
        "asana": "HG IR",
    },
    "hg_horiz_abd": {
        "label": "HG horiz abduction",
        "kind": "lt",
        "threshold": 45,
        "source": "PRI Postural Respiration",
        "asana": "HG horiz abduction",
    },
    "shoulder_flexion": {
        "label": "Shoulder flexion",
        "kind": "lt",
        "threshold": 160,
        "source": "PRI Postural Respiration",
        "asana": "shoulder flexion",
    },
    "part": {
        "label": "PART (passive abduction raise)",
        "kind": "lt",
        "threshold": 45,
        "source": "PRI Pelvis Restoration",
        "asana": "passive abduction raise",
    },
    "slr": {
        "label": "Passive SLR / leg raise",
        "kind": "slr",
        "low": 75,
        "high": 100,
        "source": "PRI Myokinematic / Pelvis (<75 limited; >100 excessive)",
        "asana": "passive leg raise",
    },
    "functional_squat": {
        "label": "Functional squat",
        "kind": "squat",
        "source": "PRI Pelvis matrices (pattern-dependent; script reports raw score only)",
        "asana": "functional squat",
    },
    "standing_reach_in": {
        "label": "Standing reach (inches from floor)",
        "kind": "reach",
        "source": "PRI Pelvis (0 = can touch; >0 = can't)",
        "asana": "toe touch",
    },
}

ALIASES = {
    "fa-ir": "fa_ir",
    "fa_ir": "fa_ir",
    "fair": "fa_ir",
    "fa-er": "fa_er",
    "fa_er": "fa_er",
    "faer": "fa_er",
    "hg-er": "hg_er",
    "hg_er": "hg_er",
    "hger": "hg_er",
    "hg-ir": "hg_ir",
    "hg_ir": "hg_ir",
    "hgir": "hg_ir",
    "hg-horiz-abd": "hg_horiz_abd",
    "hg_horiz_abd": "hg_horiz_abd",
    "horiz_abd": "hg_horiz_abd",
    "horizontal_abduction": "hg_horiz_abd",
    "shoulder_flexion": "shoulder_flexion",
    "shoulder-flexion": "shoulder_flexion",
    "hg_flexion": "shoulder_flexion",
    "part": "part",
    "passive_abduction_raise": "part",
    "slr": "slr",
    "passive_leg_raise": "slr",
    "plr": "slr",
    "functional_squat": "functional_squat",
    "squat": "functional_squat",
    "standing_reach": "standing_reach_in",
    "standing_reach_in": "standing_reach_in",
    "toe_touch": "standing_reach_in",
}


def classify_degree(key: str, value: float) -> dict[str, Any]:
    rule = CUTOFFS[key]
    kind = rule["kind"]
    out: dict[str, Any] = {
        "test": rule["label"],
        "value": value,
        "source": rule["source"],
        "asana_key": rule["asana"],
    }
    if kind == "lt":
        thr = float(rule["threshold"])
        pos = value < thr
        out["cutoff"] = f"<{thr:g}°"
        out["result"] = "Pos" if pos else "Neg"
        if "soft_low" in rule and "soft_high" in rule:
            lo, hi = float(rule["soft_low"]), float(rule["soft_high"])
            if lo <= value < hi:
                out["note"] = f"soft zone {lo:g}-{hi:g}° (PRI band); house midpoint {thr:g}°"
        return out
    if kind == "slr":
        low, high = float(rule["low"]), float(rule["high"])
        if value < low:
            out["result"] = "Pos"
            out["cutoff"] = f"<{low:g}° limited"
            out["note"] = "limited"
        elif value > high:
            out["result"] = "Pos"
            out["cutoff"] = f">{high:g}° excessive"
            out["note"] = "excessive"
        else:
            out["result"] = "Neg"
            out["cutoff"] = f"{low:g}-{high:g}°"
        return out
    if kind == "squat":
        out["result"] = "score"
        out["cutoff"] = "L AIC/PEC <3/5; Patho PEC >3/5"
        out["note"] = f"raw {value:g}/5 - apply pattern matrix"
        return out
    if kind == "reach":
        # inches from floor; 0 = touch
        pos_cant = value > 0
        out["result"] = "can't touch" if pos_cant else "can touch (0\")"
        out["cutoff"] = ">0\" = can't touch; 0\" = can"
        out["note"] = "pair with ADT/PADT for Patho PEC vs L AIC/PEC"
        return out
    out["result"] = "unknown"
    return out


def side_phrase(sides: dict[str, str]) -> str:
    """sides: {'R':'Pos','L':'Pos'} -> B / R / L / empty."""
    r, l = sides.get("R"), sides.get("L")
    if r == "Pos" and l == "Pos":
        return "B"
    if r == "Pos":
        return "R"
    if l == "Pos":
        return "L"
    return ""


def asana_lines(classified: list[dict[str, Any]]) -> list[str]:
    # Group by asana_key for R/L pairs
    by_key: dict[str, dict[str, Any]] = {}
    singles: list[str] = []
    for row in classified:
        side = row.get("side")
        key = row["asana_key"]
        if side in ("R", "L"):
            by_key.setdefault(key, {"rows": {}, "meta": row})
            by_key[key]["rows"][side] = row
        else:
            if row.get("result") == "Pos":
                singles.append(f"Pos {key}" + (f" ({row['value']:g}°)" if isinstance(row.get("value"), (int, float)) else ""))
            elif row.get("result") in ("can't touch",):
                singles.append(f"Pos toe touch - can't reach")
            elif row.get("result") == "score":
                singles.append(f"{row['value']:g} on functional squat")
    lines: list[str] = []
    for key, bundle in by_key.items():
        rows = bundle["rows"]
        results = {s: rows[s]["result"] for s in rows}
        # Only emit Pos lines for degree tests
        if any(results.get(s) == "Pos" for s in ("R", "L")):
            side = side_phrase({s: results[s] for s in ("R", "L") if s in results})
            # include values when asymmetric or helpful
            vals = []
            for s in ("R", "L"):
                if s in rows:
                    vals.append(f"{s} {rows[s]['value']:g}")
            detail = " vs ".join(vals) if len(vals) == 2 and rows.get("R", {}).get("value") != rows.get("L", {}).get("value") else ""
            line = f"Pos {side} {key}".replace("Pos  ", "Pos ")
            if detail and side != "B":
                line += f" ({detail})"
            elif detail and rows["R"]["value"] != rows["L"]["value"]:
                line += f" ({detail})"
            lines.append(line)
        # SLR excessive note
        for s, row in rows.items():
            if row.get("note") == "excessive":
                lines.append(f"Pos {s} {key} - excessive ({row['value']:g}°)")
    lines.extend(singles)
    # de-dupe while preserving order
    seen = set()
    out = []
    for ln in lines:
        if ln not in seen:
            seen.add(ln)
            out.append(ln)
    return out


def normalize_payload(data: dict[str, Any]) -> list[tuple[str, str | None, float]]:
    """Return list of (cutoff_key, side|None, value)."""
    items: list[tuple[str, str | None, float]] = []
    for raw_key, raw_val in data.items():
        key = ALIASES.get(raw_key.lower().replace(" ", "_"), ALIASES.get(raw_key.lower()))
        if key is None:
            k2 = raw_key.lower().replace("-", "_")
            key = ALIASES.get(k2)
        if key is None or key not in CUTOFFS:
            raise ValueError(f"unknown test key: {raw_key}")
        if isinstance(raw_val, dict):
            for side_raw, v in raw_val.items():
                side = side_raw.upper()[0]
                if side not in ("R", "L", "B"):
                    # allow right/left
                    sl = str(side_raw).lower()
                    if sl.startswith("r"):
                        side = "R"
                    elif sl.startswith("l"):
                        side = "L"
                    else:
                        raise ValueError(f"bad side {side_raw} for {raw_key}")
                if side == "B":
                    items.append((key, "R", float(v)))
                    items.append((key, "L", float(v)))
                else:
                    items.append((key, side, float(v)))
        else:
            items.append((key, None, float(raw_val)))
    return items


def run(data: dict[str, Any], as_json: bool) -> int:
    items = normalize_payload(data)
    classified: list[dict[str, Any]] = []
    for key, side, value in items:
        row = classify_degree(key, value)
        if side:
            row["side"] = side
        classified.append(row)

    if as_json:
        print(json.dumps({"results": classified, "asana_lines": asana_lines(classified)}, indent=2))
        return 0

    for row in classified:
        side = row.get("side", "")
        prefix = f"{side} " if side else ""
        extra = f"  [{row['note']}]" if row.get("note") else ""
        print(f"{prefix}{row['test']}: {row['value']:g}° → {row['result']}  (cutoff {row.get('cutoff', '-')}; {row['source']}){extra}")
    print()
    print("Asana Pos lines:")
    lines = asana_lines(classified)
    if not lines:
        print("  (none Pos)")
    else:
        for ln in lines:
            print(f"  - {ln}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--list", action="store_true", help="print cutoffs and exit")
    p.add_argument("--json-out", action="store_true", help="emit JSON")
    p.add_argument("--json", dest="json_in", help="JSON object of measurements")
    p.add_argument("--stdin", action="store_true", help="read JSON object from stdin")
    # convenience flags
    for side in ("r", "l"):
        p.add_argument(f"--fa-ir-{side}", type=float)
        p.add_argument(f"--fa-er-{side}", type=float)
        p.add_argument(f"--hg-er-{side}", type=float)
        p.add_argument(f"--hg-ir-{side}", type=float)
        p.add_argument(f"--hg-horiz-abd-{side}", type=float)
        p.add_argument(f"--shoulder-flexion-{side}", type=float)
        p.add_argument(f"--part-{side}", type=float)
        p.add_argument(f"--slr-{side}", type=float)
    p.add_argument("--functional-squat", type=float)
    p.add_argument("--standing-reach-in", type=float, help="inches from floor; 0 = can touch")
    return p


def flags_to_data(ns: argparse.Namespace) -> dict[str, Any]:
    data: dict[str, Any] = {}
    mapping = [
        ("fa_ir", "fa_ir"),
        ("fa_er", "fa_er"),
        ("hg_er", "hg_er"),
        ("hg_ir", "hg_ir"),
        ("hg_horiz_abd", "hg_horiz_abd"),
        ("shoulder_flexion", "shoulder_flexion"),
        ("part", "part"),
        ("slr", "slr"),
    ]
    for flag_base, key in mapping:
        sides = {}
        for s in ("r", "l"):
            v = getattr(ns, f"{flag_base}_{s}", None)
            if v is not None:
                sides[s.upper()] = v
        if sides:
            data[key] = sides
    if ns.functional_squat is not None:
        data["functional_squat"] = ns.functional_squat
    if ns.standing_reach_in is not None:
        data["standing_reach_in"] = ns.standing_reach_in
    return data


def main(argv: list[str] | None = None) -> int:
    p = build_parser()
    ns = p.parse_args(argv)
    if ns.list:
        for key, rule in CUTOFFS.items():
            if rule["kind"] == "lt":
                print(f"{key}: <{rule['threshold']}° → Pos  ({rule['source']})")
            elif rule["kind"] == "slr":
                print(f"{key}: <{rule['low']}° or >{rule['high']}° → Pos  ({rule['source']})")
            else:
                print(f"{key}: {rule['source']}")
        return 0

    data: dict[str, Any] = {}
    if ns.json_in:
        data = json.loads(ns.json_in)
    elif ns.stdin:
        data = json.load(sys.stdin)
    else:
        data = flags_to_data(ns)

    if not data:
        p.print_help()
        return 2
    try:
        return run(data, as_json=ns.json_out)
    except (ValueError, TypeError, json.JSONDecodeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
