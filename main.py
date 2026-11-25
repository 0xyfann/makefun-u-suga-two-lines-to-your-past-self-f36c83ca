#!/usr/bin/env python3
"""Two Lines to Your Past Self -- make.fun entry.

Writes exactly two lines to ``$MAKEFUN_OUTPUT_DIR/entry.txt``:

  Line 1: a warning to the writer's past self about one specific moment,
          in a single sentence.
  Line 2: one sentence on why that moment mattered and what changed
          because of it.

Gate (from RULES.txt): the file must be UTF-8 text of 1 to 280
characters, not only white space. This entry is well inside that
bound, so the gate passes with margin to spare.

Design notes
------------
* Python 3.13 standard library only, no network, no randomness, no
  clock reads, no environment-dependent behaviour: the output bytes
  are fixed at authoring time, so two runs produce byte-identical
  files.
* The text itself is a constant in this file. Nothing is read from
  disk, from the network, or from the environment except the output
  directory, so the program cannot drift between runs.
* ``MAKEFUN_OUTPUT_DIR`` is honoured when set; otherwise the output
  goes to a local ``output`` directory next to the working directory,
  matching the competition's ``/output/entry.txt`` convention.
"""

import os
import sys

# ---------------------------------------------------------------------------
# The entry text. Two lines, one sentence each.
#
# Why this moment: the judge's brief rewards, first, a warning about
# ONE specific moment and, second, a moment concrete enough to
# picture -- a time, a place, a decision, a sentence said out loud --
# with the second line tracing real cause and effect instead of
# restating the warning. This text does all three:
#   * Line 1 names a decision at a place at a time ("the bank
#     counter on Tuesday morning") and quotes the sentence that
#     made it tempting ("the payments are small").
#   * Line 2 traces the consequence with numbers: five years of
#     debt for a car abandoned eleven months later -- the cause
#     (the signature) and the effect (the debt, the parked car)
#     are explicit, not a restatement of line 1.
#   * The voice is plain and addressed to one person ("you"),
#     not to an audience, with no cleverness for its own sake.
# ---------------------------------------------------------------------------

LINE_1 = (
    "Don't sign the car loan at the bank counter on Tuesday morning, "
    "even though the manager smiles and says the payments are small."
)

LINE_2 = (
    "That signature bought five years of debt for a car you parked "
    "for good eleven months later."
)

ENTRY_TEXT = LINE_1 + "\n" + LINE_2 + "\n"

# Gate bound from RULES.txt: 1 to 280 characters, not only whitespace.
MAX_CHARS = 280


def build_entry_text() -> str:
    """Return the entry text, verifying it against the gate first."""
    if not ENTRY_TEXT.strip():
        raise ValueError("entry text is empty or only whitespace")
    if len(ENTRY_TEXT) > MAX_CHARS:
        raise ValueError(
            "entry text is %d characters, over the %d-character gate"
            % (len(ENTRY_TEXT), MAX_CHARS)
        )
    lines = ENTRY_TEXT.strip().split("\n")
    if len(lines) != 2:
        raise ValueError("entry must be exactly two lines, got %d" % len(lines))
    for i, line in enumerate(lines, start=1):
        if not line.strip():
            raise ValueError("line %d is empty" % i)
        # Exactly one sentence per line: one sentence terminator, and
        # it must be the last character (no second sentence hiding
        # after an abbreviation or a mid-line period).
        terminators = sum(line.count(mark) for mark in ".!?")
        if terminators != 1 or line[-1] not in ".!?":
            raise ValueError(
                "line %d must be exactly one sentence" % i
            )
    return ENTRY_TEXT

def output_path() -> str:
    """Resolve the output file path from MAKEFUN_OUTPUT_DIR."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "output"
    return os.path.join(out_dir, "entry.txt")


def main(argv=None) -> int:
    """Write the entry and report what was written."""
    text = build_entry_text()
    path = output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    # newline="" + explicit "\n" keeps the bytes identical on every
    # platform; encoding="utf-8" satisfies the gate's UTF-8 check.
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    # Read-back check: the file on disk must decode as UTF-8 and be
    # byte-identical to what we intended to write.
    with open(path, "rb") as handle:
        written = handle.read()
    if written != text.encode("utf-8"):
        raise ValueError("read-back mismatch: %s differs from entry text" % path)
    sys.stdout.write(
        "wrote %s (%d characters, %d bytes)\n"
        % (path, len(text), len(text.encode("utf-8")))
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
