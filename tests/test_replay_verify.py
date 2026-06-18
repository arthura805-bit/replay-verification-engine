"""Tests for replay-verification-engine.

Runs under pytest (`python -m pytest`) and also standalone without pytest
(`python tests/test_replay_verify.py`).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from replay_verify import output_hash, verify  # noqa: E402

EVENTS = [
    {"op": "set", "key": "a", "value": 1},
    {"op": "inc", "key": "a", "by": 4},
    {"op": "set", "key": "b", "value": "x"},
    {"op": "inc", "key": "a", "by": -2},
    {"op": "set", "key": "c", "value": 10},
]


def test_replay_is_deterministic():
    assert output_hash(EVENTS) == output_hash(EVENTS)


def test_event_order_matters():
    # Swap a `set` with the following `inc` on the same key (non-commutative).
    reordered = EVENTS[:]
    reordered[0], reordered[1] = reordered[1], reordered[0]
    assert output_hash(reordered) != output_hash(EVENTS)


def test_modified_event_fails_verification():
    expected = output_hash(EVENTS)
    modified = EVENTS[:]
    modified[1] = {"op": "inc", "key": "a", "by": 999}
    report = verify(modified, expected)
    assert report.status == "FAIL"
    assert report.passed is False


def test_report_contains_pass_and_fail():
    good = verify(EVENTS, output_hash(EVENTS))
    bad = verify(EVENTS[:-1], output_hash(EVENTS))
    assert good.status == "PASS"
    assert bad.status == "FAIL"
    assert "PASS" in str(good)
    assert "FAIL" in str(bad)


def _run_standalone() -> int:
    failures = 0
    for fn in (
        test_replay_is_deterministic,
        test_event_order_matters,
        test_modified_event_fails_verification,
        test_report_contains_pass_and_fail,
    ):
        try:
            fn()
        except AssertionError as exc:  # pragma: no cover
            failures += 1
            print("FAIL:", fn.__name__, exc)
    print("PASS" if failures == 0 else f"{failures} FAILED")
    return failures


if __name__ == "__main__":
    raise SystemExit(_run_standalone())
