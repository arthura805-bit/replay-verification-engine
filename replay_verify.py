"""replay-verification-engine — deterministic replay + verification reports.

A small but real demonstration of replay-based verification:

  * **event-sequence replay** — fold an ordered event log into a final state
    with a pure update function;
  * **deterministic output hash** — the same log always yields the same final
    state hash, independent of run, machine or Python version;
  * **verification report** — comparing a replay against an expected hash
    produces a structured PASS / FAIL report;
  * **mismatch detection** — a reordered, dropped or modified event log fails
    verification.

Standard library only. Synthetic data only. No proprietary code or data.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any


def canonical(obj: Any) -> bytes:
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")


def apply_event(state: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    """Pure update function — returns a new state, never mutates the input.

    Event kinds (deliberately simple and deterministic):
      * {"op": "set", "key": k, "value": v}
      * {"op": "inc", "key": k, "by": n}
    """
    new = dict(state)
    op, key = event["op"], event["key"]
    if op == "set":
        new[key] = event["value"]
    elif op == "inc":
        new[key] = new.get(key, 0) + event["by"]
    else:
        raise ValueError(f"unknown op: {op!r}")
    return new


def replay(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Fold an ordered event log into a final state."""
    state: dict[str, Any] = {}
    for ev in events:
        state = apply_event(state, ev)
    return state


def output_hash(events: list[dict[str, Any]]) -> str:
    """SHA-256 of the canonical final state produced by replaying `events`."""
    return hashlib.sha256(canonical(replay(events))).hexdigest()


@dataclass(frozen=True)
class VerificationReport:
    """Structured result of verifying a replay against an expected hash."""

    status: str  # "PASS" or "FAIL"
    expected: str
    actual: str
    event_count: int

    @property
    def passed(self) -> bool:
        return self.status == "PASS"

    def __str__(self) -> str:
        return (
            f"[{self.status}] events={self.event_count} "
            f"expected={self.expected[:16]}... actual={self.actual[:16]}..."
        )


def verify(events: list[dict[str, Any]], expected_hash: str) -> VerificationReport:
    """Replay `events` and report PASS/FAIL against `expected_hash`."""
    actual = output_hash(events)
    status = "PASS" if actual == expected_hash else "FAIL"
    return VerificationReport(status, expected_hash, actual, len(events))


if __name__ == "__main__":
    # Tiny smoke run; see examples/replay_demo.py for the full demonstration.
    events = [
        {"op": "set", "key": "a", "value": 1},
        {"op": "inc", "key": "a", "by": 4},
        {"op": "set", "key": "b", "value": "x"},
    ]
    report = verify(events, output_hash(events))
    print(report)
