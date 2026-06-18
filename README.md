# replay-verification-engine

A small but real Python project demonstrating **replay-based verification** —
the core idea behind reproducible workflows and reliability checks.

- **event-sequence replay** — fold an ordered event log into a final state with
  a pure update function
- **deterministic output hash** — the same log always yields the same final
  state hash, independent of run, machine or Python version
- **verification report** — a structured PASS / FAIL result (`VerificationReport`
  dataclass)
- **mismatch detection** — a reordered, dropped or modified event log fails
  verification

Standard library at runtime. Synthetic data only. No proprietary code or data.

## Project layout

```
replay_verify.py            # replay, output_hash, VerificationReport, verify
examples/replay_demo.py     # end-to-end demonstration
tests/test_replay_verify.py # tests (pytest or standalone)
requirements.txt            # dev-only: pytest
```

## Run

```bash
python examples/replay_demo.py     # demonstration
python -m pytest                   # tests (if pytest installed)
python tests/test_replay_verify.py # tests without any dependency
```

## How it works

`apply_event` is a pure function (new state in, never mutates), so replaying a
log is deterministic. `output_hash` is SHA-256 over the canonical
(`sort_keys=True`) serialization of the final state, and `verify` returns a
`VerificationReport` comparing a replay against an expected hash. Because the
serialization is canonical and the events carry no clock or randomness, the
output hash is stable across runs and Python versions — and any change to the
event sequence (reorder, drop, modify) flips the report to FAIL.

## Scope

A focused demonstration of mechanism and discipline — pure replay, deterministic
hashing, sequence validation and structured reporting. Not a product, not a
benchmark.

## License

MIT — see [LICENSE](LICENSE).
