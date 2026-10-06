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

### Tool call: ls
{"path": "workspace/bookings"}

### Tool result
['/workspace/bookings/__init__.py', '/workspace/bookings/__pycache__/', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py']

### Tool call: ls
{"path": "workspace/tests"}

### Tool result
['/workspace/tests/__pycache__/', '/workspace/tests/test_bookings.py']

### Tool call: read_file
{"file_path": "skills/python-code-quality-and-testing-rules/SKILL.md", "limit": 1000}

### Tool result
@@ lines 1-10 of 10 @@
---
name: python-code-quality-and-testing-rules
description: Use when modifying Python packages, adding bug fixes, or writing tests.
---
# Python Code Quality and Testing Rules

- **Do Not Modify Original Tests:** Never edit existing test files provided in the repository. Add new test files (e.g., `tests/test_regressions.py`) if additional tests are needed.
- **Type Annotations:** Ensure *every* public function (any function whose name does not start with an underscore `_`) has explicit type annotations on all parameters and on its return value.
- **Regression Tests:** Add a regression test file (`tests/test_regressions.py`) containing at least one test function per fixed bug (minimum 3 tests total), and verify that all tests pass.
- **Changelog Updates:** Record each bug fix in `CHANGELOG.md` under the heading `## Unreleased` as a bullet point in the format `- fix(<function name>): <short description>` (at least 3 bullets).

### Tool call: execute
{"command": "pytest workspace/tests/test_bookings.py"}

### Tool result
[stderr] /usr/bin/bash: line 1: pytest: command not found

Exit code: 127
[Command failed with exit code 127]

### Tool call: execute
{"command": "python3 -m pytest workspace/tests/test_bookings.py"}

### Tool result
============================= test session starts =============================
platform win32 -- Python 3.11.7, pytest-8.4.2, pluggy-1.6.0
rootdir: ~\AppData\Local\Temp\lab_sandbox_vh4ojcg1
plugins: anyio-4.15.1, langsmith-0.14.4, asyncio-1.4.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 0 items / 1 error

=================================== ERRORS ====================================
______________ ERROR collecting workspace/tests/test_bookings.py ______________
ImportError while importing test module '~\AppData\Local\Temp\lab_sandbox_vh4ojcg1\workspace\tests\test_bookings.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
..\..\Programs\Python\Python311\Lib\importlib\__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
D:\AI_20K\Day 20 - Track 3 - Multi Agent System\K4-DAY20-MULTIAGENTS-DuongDinhLong-2A202602474\tasks\code-eval\workspace\tests\test_bookings.py:1: in <module>
    from bookings.billing import billable_blocks
E   ModuleNotFoundError: No module named 'bookings'
=========================== short test summary info ===========================
ERROR workspace/tests/test_bookings.py
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
============================== 1 error in 0.43s ===============================

### Tool call: execute
{"command": "export PYTHONPATH=$PYTHONPATH:$(pwd)/workspace && python3 -m pytest workspace/tests/test_bookings.py"}

### Tool result
============================= test session starts =============================
platform win32 -- Python 3.11.7, pytest-8.4.2, pluggy-1.6.0
rootdir: ~\AppData\Local\Temp\lab_sandbox_vh4ojcg1
plugins: anyio-4.15.1, langsmith-0.14.4, asyncio-1.4.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 0 items / 1 error

=================================== ERRORS ====================================
______________ ERROR collecting workspace/tests/test_bookings.py ______________
ImportError while importing test module '~\AppData\Local\Temp\lab_sandbox_vh4ojcg1\workspace\tests\test_bookings.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
..\..\Programs\Python\Python311\Lib\importlib\__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
D:\AI_20K\Day 20 - Track 3 - Multi Agent System\K4-DAY20-MULTIAGENTS-DuongDinhLong-2A202602474\tasks\code-eval\workspace\tests\test_bookings.py:1: in <module>
    from bookings.billing import billable_blocks
E   ModuleNotFoundError: No module named 'bookings'
=========================== short test summary info ===========================
ERROR workspace/tests/test_bookings.py
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
============================== 1 error in 0.41s ===============================

### Tool call: execute
{"command": "PYTHONPATH=workspace python3 -m pytest workspace/tests/test_bookings.py"}

### Tool result
============================= test session starts =============================
platform win32 -- Python 3.11.7, pytest-8.4.2, pluggy-1.6.0
rootdir: ~\AppData\Local\Temp\lab_sandbox_vh4ojcg1
plugins: anyio-4.15.1, langsmith-0.14.4, asyncio-1.4.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 3 items

workspace\tests\test_bookings.py FF.                                     [100%]

================================== FAILURES ===================================
______________________ test_total_minutes_mixed_formats _______________________

    def test_total_minutes_mixed_formats():
>       assert total_minutes(["1h30m", "2h"]) == 210
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

D:\AI_20K\Day 20 - Track 3 - Multi Agent System\K4-DAY20-MULTIAGENTS-DuongDinhLong-2A202602474\tasks\code-eval\workspace\tests\test_bookings.py:6: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
workspace\bookings\schedule.py:7: in total_minutes
    return sum(parse_duration(d) for d in durations)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
workspace\bookings\schedule.py:7: in <genexpr>
    return sum(parse_duration(d) for d in durations)
               ^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

text = '2h'

    def parse_duration(text):
        """Convert a duration string to whole minutes (int).
    
        Supported f

### Tool call: read_file
{"file_path": "workspace/bookings/timeutil.py"}

### Tool result
@@ lines 1-19 of 19 @@
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

### Tool call: edit_file
{"file_path": "workspace/bookings/timeutil.py", "new_string": "def parse_duration(text: str) -> int:\n    \"\"\"Convert a duration string to whole minutes (int).\n\n    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare number means minutes\n    Surrounding whitespace is ignored.\n    \"\"\"\n    text = text.strip()\n    if \":\" in text:\n        hours, minutes = map(int, text.split(\":\"))\n        return hours * 60 + minutes\n    \n    m_h_m = re.fullmatch(r\"(\\d+)h(\\d+)m\", text)\n    if m_h_m:\n        return int(m_h_m.group(1)) * 60 + int(m_h_m.group(2))\n    \n    m_h = re.fullmatch(r\"(\\d+)h\", text)\n    if m_h:\n        return int(m_h.group(1)) * 60\n    \n    m_m = re.fullmatch(r\"(\\d+)m\", text)\n    if m_m:\n        return int(m_m.group(1))\n    \n    if text.isdigit():\n        return int(text)\n    \n    raise ValueError(f\"bad duration: {text!r}\")", "old_string": "def parse_duration(text):\n    \"\"\"Convert a duration string to whole minutes (int).\n\n    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare number means minutes\n    Surrounding whitespace is ignored.\n    \"\"\"\n    m = re.fullmatch(r\"(\\d+)h(\\d+)m\", text.strip())\n    if not m:\n        raise ValueError(f\"bad duration: {text!r}\")\n    return int(m.group(1)) * 60 + int(m.group(2))"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/timeutil.py'

### Tool call: read_file
{"file_path": "workspace/bookings/billing.py"}

### Tool result
@@ lines 1-11 of 11 @@
"""Billing rules."""


def billable_blocks(minutes, block=15):
    """Number of billable blocks for a booking.

    A partial block is billed as a full block (always round UP):
    16 minutes with 15-minute blocks -> 2 blocks.
    `minutes` must be >= 0; a negative value raises ValueError.
    """
    return round(minutes / block)

### Tool call: edit_file
{"file_path": "workspace/bookings/billing.py", "new_string": "import math\n\n\ndef billable_blocks(minutes: int, block: int = 15) -> int:\n    \"\"\"Number of billable blocks for a booking.\n\n    A partial block is billed as a full block (always round UP):\n    16 minutes with 15-minute blocks -> 2 blocks.\n    `minutes` must be >= 0; a negative value raises ValueError.\n    \"\"\"\n    if minutes < 0:\n        raise ValueError(\"minutes must be >= 0\")\n    return math.ceil(minutes / block)", "old_string": "def billable_blocks(minutes, block=15):\n    \"\"\"Number of billable blocks for a booking.\n\n    A partial block is billed as a full block (always round UP):\n    16 minutes with 15-minute blocks -> 2 blocks.\n    `minutes` must be >= 0; a negative value raises ValueError.\n    \"\"\"\n    return round(minutes / block)"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/billing.py'

### Tool call: execute
{"command": "PYTHONPATH=workspace python3 -m pytest workspace/tests/test_bookings.py"}

### Tool result
============================= test session starts =============================
platform win32 -- Python 3.11.7, pytest-8.4.2, pluggy-1.6.0
rootdir: ~\AppData\Local\Temp\lab_sandbox_vh4ojcg1
plugins: anyio-4.15.1, langsmith-0.14.4, asyncio-1.4.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 3 items

workspace\tests\test_bookings.py ...                                     [100%]

============================== 3 passed in 0.08s ==============================

[Command succeeded with exit code 0]

### Tool call: write_file
{"content": "import pytest\nfrom bookings.billing import billable_blocks\nfrom bookings.timeutil import parse_duration\nfrom bookings.schedule import total_minutes\n\ndef test_parse_duration_all_formats():\n    assert parse_duration(\"1h30m\") == 90\n    assert parse_duration(\"2h\") == 120\n    assert parse_duration(\"45m\") == 45\n    assert parse_duration(\"1:30\") == 90\n    assert parse_duration(\"45\") == 45\n\ndef test_billable_blocks_edge_cases():\n    assert billable_blocks(0) == 0\n    assert billable_blocks(15) == 1\n    assert billable_blocks(16) == 2\n    with pytest.raises(ValueError):\n        billable_blocks(-1)\n\ndef test_total_minutes_empty():\n    assert total_minutes([]) == 0\n", "file_path": "workspace/tests/test_regressions.py"}

### Tool result
Updated file /workspace/tests/test_regressions.py

### Tool call: execute
{"command": "PYTHONPATH=workspace python3 -m pytest workspace/tests/test_regressions.py"}

### Tool result
============================= test session starts =============================
platform win32 -- Python 3.11.7, pytest-8.4.2, pluggy-1.6.0
rootdir: ~\AppData\Local\Temp\lab_sandbox_vh4ojcg1
plugins: anyio-4.15.1, langsmith-0.14.4, asyncio-1.4.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 3 items

workspace\tests\test_regressions.py ...                                  [100%]

============================== 3 passed in 0.06s ==============================

[Command succeeded with exit code 0]

### Tool call: read_file
{"file_path": "workspace/bookings/schedule.py"}

### Tool result
@@ lines 1-17 of 17 @@
"""Schedule helpers."""
from .timeutil import parse_duration


def total_minutes(durations):
    """Total minutes of a list of duration strings."""
    return sum(parse_duration(d) for d in durations)


def add_slot(slot, slots=[]):
    """Return a NEW list containing the given slots plus `slot`.

    Separate calls must not share state: calling add_slot("a") and then
    add_slot("b") returns ["a"] and then ["b"].
    """
    slots.append(slot)
    return slots

### Tool call: edit_file
{"file_path": "workspace/bookings/schedule.py", "new_string": "from typing import List\nfrom .timeutil import parse_duration\n\n\ndef total_minutes(durations: List[str]) -> int:\n    \"\"\"Total minutes of a list of duration strings.\"\"\"\n    return sum(parse_duration(d) for d in durations)\n\n\ndef add_slot(slot: str, slots: List[str] = None) -> List[str]:\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    if slots is None:\n        slots = []\n    return slots + [slot]", "old_string": "from .timeutil import parse_duration\n\n\ndef total_minutes(durations):\n    \"\"\"Total minutes of a list of duration strings.\"\"\"\n    return sum(parse_duration(d) for d in durations)\n\n\ndef add_slot(slot, slots=[]):\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    slots.append(slot)\n    return slots"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/schedule.py'