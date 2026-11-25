# Build Notes — Two Lines to Your Past Self

Competition: `u-suga-two-lines-to-your-past-self-f36c83ca` ($2, escrowed)
Deadline: 26 Nov 2026, 15:40 WIB (08:40 UTC)
Account: @0xyfann — repo `makefun-u-suga-two-lines-to-your-past-self-f36c83ca`

## What was built

`main.py` (Python 3.13, standard library only) writes the entry text to
`$MAKEFUN_OUTPUT_DIR/entry.txt`. The text is a fixed constant in the
file, validated at run time against the competition gate before it is
written:

- UTF-8, 1–280 characters (this entry: see local test below)
- exactly two lines, each one sentence, neither line empty
- no network, no randomness, no clock reads — two runs are
  byte-identical by construction

The entry itself:

> Don't sign the car loan at the bank counter on Tuesday morning, even
> though the manager smiles and says the payments are small.
> That signature bought five years of debt for a car you parked for
> good eleven months later.

Why this text: the judge brief ranks (1) a warning about one specific
moment, (2) a moment concrete enough to picture, (3) a second line that
traces real cause and effect. Line 1 names a decision, a place, a time,
and a sentence said out loud; line 2 quantifies the consequence (five
years of debt, car parked after eleven months) instead of restating the
warning. Plain voice, addressed to one person.

## How to run

```bash
python3 main.py
# writes output/entry.txt (default when MAKEFUN_OUTPUT_DIR is unset)

MAKEFUN_OUTPUT_DIR=/tmp/out1 python3 main.py
# writes /tmp/out1/entry.txt
```

Requirements: Python 3.13, nothing to install. Runs in well under a
second, negligible memory.

## Revision history (this session)

- v1: wrote `main.py` (constant text + gate validation), ran twice —
  identical output, 220 chars.
- v2 (revision): stricter validation — each line must contain exactly
  one sentence terminator, as its last character — plus a read-back
  check that the file on disk is byte-identical UTF-8. Re-ran twice
  (see below); output unchanged.

## Local test (run 2026-11-25, after revision)

Two runs with different `MAKEFUN_OUTPUT_DIR` values produced
byte-identical `entry.txt` files:

- SHA-256 (both runs): `361287740d015751b852ca5449b1224b334316663c930c66e183c1b36769045a`
- `cmp` result: IDENTICAL
- Length: 220 characters including trailing newline (219 stripped),
  220 bytes — inside the 1–280 character gate (60 chars of headroom)
- Lines: 2 (line 1: 127 chars, line 2: 91 chars), one sentence each
- Runtime: ~0.03–0.04 s per run (limit 60 s); `py_compile` clean
- Note: local Python is 3.12.3; the code uses stdlib only and is
  compatible with the grader's Python 3.13.
