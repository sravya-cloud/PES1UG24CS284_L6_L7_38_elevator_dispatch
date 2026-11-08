# Lab 7: Fuzz Testing for Input Validation Bugs
## Elevator Dispatch System

### 1. Objective

The objective of this lab is to use property-based fuzz testing with the `hypothesis` library to discover input validation bugs in the Elevator Dispatch application, and then harden the application against every malformed input the fuzzer finds.

Unlike unit tests, which check the cases the developer thought of, a fuzzer generates hundreds of random and malformed inputs automatically and shrinks any failure down to the smallest input that still reproduces it.

### 2. Project Structure

```text
lab7/
|-- elevator_dispatch.py
|-- test_elevator_dispatch.py
|-- README.md
`-- SCREENSHOTS/
    |-- 1_buggy_app_output.png
    |-- 2_tests_failing.png
    |-- 3_fixed_app_output.png
    `-- 4_tests_passing.png
```

### 3. Software Requirements

- Python 3.8+
- hypothesis
- pytest

Install dependencies:

```bash
pip install hypothesis pytest
```

### 4. Functions Under Test

| Function | Expected input | Returns |
|----------|----------------|---------|
| `parse_request(text)` | `'FROM->TO'`, e.g. `5->9` | `(start, end)` tuple of floors |
| `total_travel(floors_csv)` | CSV of floors, e.g. `1,5,3,9` | Total distance travelled |
| `load_percent(text)` | `'X of Y'`, e.g. `450 of 630` | Load as a percentage |

### 5. Fuzz Test Design

Each function is checked for two properties rather than for individual expected values:

1. **Robustness** - the function must never raise, whatever it is handed.
2. **Correctness** - whenever it does return a value, that value must satisfy the function's contract (floors in range, distance non-negative, percentage between 0 and 100).

The fuzzing strategy mixes free-form Unicode text with non-string types so that both near-misses and complete nonsense are explored:

```python
MESSY_INPUT = st.one_of(
    st.none(), st.text(), st.integers(), st.floats(),
    st.booleans(), st.lists(st.integers()), st.binary(),
)
```

Three further round-trip tests confirm that hardening the code did not break its behaviour on valid input.

**Command to execute:**

```bash
python -m pytest test_elevator_dispatch.py -v
```

### 6. Bugs Discovered by Fuzzing

Running the fuzz tests against the original application produced **5 failed, 6 passed**. The failing inputs Hypothesis shrank to were:

| Function | Minimal failing input | Exception |
|----------|----------------------|-----------|
| `parse_request` | `None` | `AttributeError: 'NoneType' object has no attribute 'split'` |
| `parse_request` | `''` | `ValueError: not enough values to unpack (expected 2, got 1)` |
| `parse_request` | `b''` | `TypeError: a bytes-like object is required, not 'str'` |
| `total_travel` | `None` | `AttributeError: 'NoneType' object has no attribute 'split'` |
| `total_travel` | `''` | `ValueError: invalid literal for int() with base 10: ''` |
| `total_travel` | `b''` | `TypeError: a bytes-like object is required, not 'str'` |
| `load_percent` | `None` | `AttributeError: 'NoneType' object has no attribute 'split'` |
| `load_percent` | `''` | `ValueError: not enough values to unpack (expected 2, got 1)` |
| `load_percent` | `'1 of 0'` | `ZeroDivisionError: integer division or modulo by zero` |
| `load_percent` | `'2 of 1'` | Returned `200`, a percentage above 100 |

The three round-trip tests passed even before the fix, confirming that the bugs were in input validation and not in the underlying arithmetic.

### 7. Fixes Applied

Every function was rewritten to validate its input before using it, and to return `None` instead of raising when the input cannot be understood. Returning `None` rather than propagating an exception keeps the caller in control and means no user-supplied string can take the dispatcher down.

| Defect class | Fix |
|--------------|-----|
| Non-string input (`None`, `int`, `bytes`, `list`) | `_clean_text` rejects anything that is not a `str` |
| Empty or whitespace-only input | Rejected after stripping |
| Missing or repeated separator (`5 to 9`, `1->2->3`) | Split result must contain exactly two parts |
| Non-numeric tokens (`one,two`) | Strict regex `[+-]?[0-9]+` instead of bare `int()` |
| Empty CSV entries (`1,,3`) | Each token validated individually |
| Floors outside the building | Range check against `MIN_FLOOR` and `MAX_FLOOR` |
| Division by zero (`450 of 0`) | Capacity must be positive |
| Percentage above 100 (`2 of 1`) | Load above capacity treated as a faulty reading |
| Negative load | Load must be non-negative |
| Oversized input (denial of service) | `MAX_INPUT_LENGTH` and `MAX_FLOORS_PER_TRIP` caps |

The strict regex is worth noting: Python's built-in `int()` silently accepts underscores (`int("1_0") == 10`), surrounding whitespace, and non-ASCII digits. The regex rejects all of these, so only genuine ASCII integers are accepted.

`main()` now reports rejected input with a readable message instead of a traceback.

### 8. Results

| Stage | Command | Result |
|-------|---------|--------|
| Buggy application | `python elevator_dispatch.py` | Crashes with a traceback on malformed input |
| Fuzz tests vs. buggy code | `python -m pytest test_elevator_dispatch.py -v` | **5 failed, 6 passed** |
| Fixed application | `python elevator_dispatch.py` | Rejects malformed input with a clear message |
| Fuzz tests vs. fixed code | `python -m pytest test_elevator_dispatch.py -v` | **11 passed** |

Behaviour on valid input is unchanged:

```text
From and To: (5, 9)
Floors Travelled: 12
Load Percent: 71
```

### 9. Conclusion

Fuzz testing of the Elevator Dispatch application was completed successfully.

Hypothesis automatically discovered ten distinct input validation defects across three functions - crashes from `None`, empty strings, non-string types, non-numeric tokens, and a division by zero, plus a logic defect that reported loads above 100%. None of these were covered by the existing unit tests.

After applying defensive input validation, all 11 property-based tests pass and the application degrades gracefully on malformed input rather than crashing. The exercise demonstrates that property-based fuzzing finds classes of defect that example-based unit tests systematically miss, because the fuzzer is not limited to the inputs the developer already had in mind.
