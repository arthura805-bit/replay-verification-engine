"""End-to-end demonstration of replay-verification-engine.

Run from the repo root:
    python examples/replay_demo.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from replay_verify import output_hash, replay, verify  # noqa: E402


def main() -> int:
    events = [
        {"op": "set", "key": "a", "value": 1},
        {"op": "inc", "key": "a", "by": 4},
        {"op": "set", "key": "b", "value": "x"},
        {"op": "inc", "key": "a", "by": -2},
        {"op": "set", "key": "c", "value": 10},
    ]

    expected = output_hash(events)
    print(f"final state : {replay(events)}")
    print(f"output hash : {expected}")
    print()

    print("verification reports:")
    print(f"  same log     : {verify(events, expected)}")

    reordered = events[:]
    reordered[0], reordered[1] = reordered[1], reordered[0]
    print(f"  reordered    : {verify(reordered, expected)}")

    dropped = events[:-1]
    print(f"  dropped event: {verify(dropped, expected)}")

    ok = (
        verify(events, expected).passed
        and not verify(reordered, expected).passed
        and not verify(dropped, expected).passed
    )
    print(f"\nall checks passed: {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
