# replay-verification-engine

Deterministic event replay and verification reports in Python — the core idea
behind reproducible workflows and reliability checks.

## What this demonstrates
- **Event-sequence replay** — fold an ordered event log into a final state with
  a pure update function (`EventRecord` dataclass for typed events).
- **Deterministic output hash** — the same log always yields the same final
  state hash, independent of run, machine or Python version.
- **Verification report** — a structured PASS / FAIL result (`VerificationReport`
  dataclass).
- **Mismatch detection** — a reordered, dropped or modified event log fails
  verification.

## Run
```bash
python examples/replay_demo.py
```

## Run tests
```bash
python -m pytest                    # if pytest is installed
python tests/test_replay_verify.py  # standalone, no dependencies
```

## How it works
`apply_event` is a pure function (new state in, never mutates), so replaying a
log is deterministic. `output_hash` is SHA-256 over the canonical
(`sort_keys=True`) serialization of the final state, and `verify` returns a
`VerificationReport` comparing a replay against an expected hash. Any change to
the event sequence flips the report to FAIL.

## Scope
A focused demonstration of mechanism and discipline — pure replay, deterministic
hashing, sequence validation and structured reporting. Standard library at
runtime, synthetic data only. Not a product, not a benchmark.

## License
MIT — see [LICENSE](LICENSE).
