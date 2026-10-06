### Human
The test suite of the `bookings` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Tool call: ls
{"path": "workspace"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/', '/workspace/tests/']

### Tool call: task
{"description": "Explore the workspace, examine the bookings package files and tests, run pytest via execute, and understand why the test suite is failing and what needs to be fixed. Report all findings.", "subagent_type": "explorer"}

### Tool result
I have explored the workspace, examined the `bookings` package files and tests, and run pytest. 

Here is a comprehensive summary of the findings, why the test suite is failing, and what needs to be fixed.

---

### 1. Workspace Structure & Files
- **`workspace/bookings/__init__.py`**: Package initialization.
- **`workspace/bookings/timeutil.py`**: Contains `parse_duration(text)` for parsing duration strings.
- **`workspace/bookings/billing.py`**: Contains `billable_blocks(minutes, block=15)` for calculating billable blocks.
- **`workspace/bookings/schedule.py`**: Contains `total_minutes(durations)` and `add_slot(slot, slots=[])`.
- **`workspace/tests/test_bookings.py`**: Test suite verifying `total_minutes`, `billable_blocks`, and `add_slot`.
- **`workspace/README.md`**: Provides instructions to run tests (`cd workspace && python -m pytest tests -q`).

---

### 2. Why the Test Suite is Failing

When running pytest via `cd workspace && python -m pytest tests -q`, 2 out of 3 tests fail (`test_total_minutes_mixed_formats` and `test_billable_blocks_rounds_up`), while `test_add_slot_single_call` passes.

#### Failure 1: `test_total_minutes_mixed_formats` (`ValueError: bad duration: '2h'`)
- **Test expectation**: `total_minutes(["1h30m", "2h"]) == 210`
- **Root cause in `bookings/timeutil.py`**:
  - The docstring specifies multiple supported formats: `"1h30m"`, `"2h"`, `"45m"`, `"1:30"`, and `"45"`.
  - However, the implementation of `parse_duration(text)` strictly uses a regular 

### Tool call: task
{"description": "Read all source files in workspace/bookings/ (`timeutil.py`, `billing.py`, `schedule.py`, `__init__.py`) and `tests/test_bookings.py` using read_file to inspect their exact contents and docstrings before making any edits.", "subagent_type": "explorer"}

### Tool result
I have read all requested source files in `workspace/bookings/` (`timeutil.py`, `billing.py`, `schedule.py`, `__init__.py`) and `tests/test_bookings.py` using `read_file`. Here are the contents:

### 1. `workspace/bookings/timeutil.py`
```python
"""Time helpers for the bookings package."""
import re


def parse_duration(text):
    """Convert a duration string to whole minutes (int).

    Supported formats:
      "1h30m" -> 90
      "2h"    -> 120
      "45m"   -> 45
      "1:30"  -> 90
      "45"    -> 45    # a bare number means minutes
    Surrounding whitespace is ignored.
    """
    m = re.fullmatch(r"(\d+)h(\d+)m", text.strip())
    if not m:
        raise ValueError(f"bad duration: {text!r}")
    return int(m.group(1)) * 60 + int(m.group(2))
```

### 2. `workspace/bookings/billing.py`
```python
"""Billing rules."""


def billable_blocks(minutes, block=15):
    """Number of billable blocks for a booking.

    A partial block is billed as a full block (always round UP):
    16 minutes with 15-minute blocks -> 2 blocks.
    `minutes` must be >= 0; a negative value raises ValueError.
    """
    return round(minutes / block)
```

### 3. `workspace/bookings/schedule.py`
```python
"""Schedule helpers."""
from .timeutil import parse_duration


def total_minutes(durations):
    """Total minutes of a list of duration strings."""
    return sum(parse_duration(d) for d in durations)


def add_slot(slot, slots=[]):
    """Return a NEW list containing the given slots plus `slot`.



### Tool call: task
{"subagent_type": "explorer", "description": "Run pytest using the execute tool to verify the test suite failure state before making changes."}

### Tool result
I ran `python3 -m pytest -o pythonpath=workspace workspace/tests` using the `execute` tool, and verified the initial test suite failure state:

- **2 tests failed** (`test_total_minutes_mixed_formats` and `test_billable_blocks_rounds_up`)
- **1 test passed** (`test_calendar_export_basic`)

### Tool call: task
{"description": "Design and implement the fixes for bookings package:\n1. `workspace/bookings/timeutil.py`: Implement `parse_duration(text)` supporting all specified formats (`1h30m`, `2h`, `45m`, `1:30`, `45`, whitespace handling, invalid handling raising ValueError).\n2. `workspace/bookings/billing.py`: Implement `billable_blocks(minutes, block=15)` to correctly round up (ceiling division) and raise `ValueError` for negative minutes.\n3. `workspace/bookings/schedule.py`: Fix `add_slot(slot, slots=None)` mutable default argument bug to ensure separate calls do not share state.\n\nUse implementer agent / write_file or edit_file.", "subagent_type": "implementer"}