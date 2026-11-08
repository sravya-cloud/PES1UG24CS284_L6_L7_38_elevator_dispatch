"""
Lab 7: Fuzz Testing with Hypothesis
Property-based tests for the Elevator Dispatch module.

Each function is tested for two properties:
  1. Robustness  - it must never crash, whatever it is given.
  2. Correctness - whenever it does return a value, that value must
                   satisfy the function's documented contract.

The same file is run twice: once against the buggy module (tests fail)
and once against the hardened module (tests pass).

Run with:  python -m pytest test_elevator_dispatch.py -v
"""

from hypothesis import given, settings, strategies as st

from elevator_dispatch import parse_request, total_travel, load_percent

# Floor range the hardened module accepts. Declared here as well as in
# elevator_dispatch.py so that this test file also runs against the
# original buggy module, which does not define them.
MIN_FLOOR = -10
MAX_FLOOR = 200

# A strategy that mixes free-form Unicode text, plausible-looking inputs
# and non-string types, so the fuzzer explores both near-misses and
# complete nonsense.
MESSY_INPUT = st.one_of(
    st.none(),
    st.text(),
    st.integers(),
    st.floats(),
    st.booleans(),
    st.lists(st.integers()),
    st.binary(),
)


# ---------------------------------------------------------------------------
# parse_request
# ---------------------------------------------------------------------------

@given(MESSY_INPUT)
@settings(max_examples=300)
def test_parse_request_no_crash(s):
    """parse_request must never raise, no matter what it is handed."""
    try:
        parse_request(s)
    except Exception as e:
        assert False, f"parse_request crashed on {s!r} with: {type(e).__name__}: {e}"


@given(MESSY_INPUT)
@settings(max_examples=300)
def test_parse_request_contract(s):
    """When parse_request returns a value it must be a valid floor pair."""
    try:
        result = parse_request(s)
    except Exception:
        return  # crashes are reported by test_parse_request_no_crash
    if result is None:
        return
    assert isinstance(result, tuple), f"expected tuple, got {type(result).__name__}"
    assert len(result) == 2, f"expected 2 floors, got {len(result)}"
    start, end = result
    assert isinstance(start, int) and isinstance(end, int)
    assert MIN_FLOOR <= start <= MAX_FLOOR, f"start floor {start} out of range"
    assert MIN_FLOOR <= end <= MAX_FLOOR, f"end floor {end} out of range"


@given(st.integers(MIN_FLOOR, MAX_FLOOR), st.integers(MIN_FLOOR, MAX_FLOOR))
def test_parse_request_roundtrip(start, end):
    """A well-formed request must parse back to the floors it was built from."""
    assert parse_request(f"{start}->{end}") == (start, end)


# ---------------------------------------------------------------------------
# total_travel
# ---------------------------------------------------------------------------

@given(MESSY_INPUT)
@settings(max_examples=300)
def test_total_travel_no_crash(s):
    """total_travel must never raise, no matter what it is handed."""
    try:
        total_travel(s)
    except Exception as e:
        assert False, f"total_travel crashed on {s!r} with: {type(e).__name__}: {e}"


@given(MESSY_INPUT)
@settings(max_examples=300)
def test_total_travel_contract(s):
    """Distance travelled can never be negative or a non-integer."""
    try:
        result = total_travel(s)
    except Exception:
        return  # crashes are reported by test_total_travel_no_crash
    if result is None:
        return
    assert isinstance(result, int) and not isinstance(result, bool)
    assert result >= 0, f"negative distance {result} from {s!r}"


@given(st.lists(st.integers(MIN_FLOOR, MAX_FLOOR), min_size=1, max_size=20))
def test_total_travel_matches_manual_sum(floors):
    """The total must equal the sum of the gaps between consecutive floors."""
    expected = sum(abs(floors[i + 1] - floors[i]) for i in range(len(floors) - 1))
    assert total_travel(",".join(str(f) for f in floors)) == expected


@given(st.integers(MIN_FLOOR, MAX_FLOOR))
def test_total_travel_single_floor_is_zero(floor):
    """Staying on one floor means no travel."""
    assert total_travel(str(floor)) == 0


# ---------------------------------------------------------------------------
# load_percent
# ---------------------------------------------------------------------------

@given(MESSY_INPUT)
@settings(max_examples=300)
def test_load_percent_no_crash(s):
    """load_percent must never raise, no matter what it is handed."""
    try:
        load_percent(s)
    except Exception as e:
        assert False, f"load_percent crashed on {s!r} with: {type(e).__name__}: {e}"


@given(MESSY_INPUT)
@settings(max_examples=300)
def test_load_percent_contract(s):
    """A percentage must be an integer between 0 and 100."""
    try:
        result = load_percent(s)
    except Exception:
        return  # crashes are reported by test_load_percent_no_crash
    if result is None:
        return
    assert isinstance(result, int) and not isinstance(result, bool)
    assert 0 <= result <= 100, f"percentage out of range: {result} from {s!r}"


@given(st.integers(0, 10000), st.integers(1, 10000))
def test_load_percent_matches_manual_ratio(load, capacity):
    """For a sane load and capacity the result must match the hand calculation."""
    result = load_percent(f"{load} of {capacity}")
    if load > capacity:
        # An overloaded car is invalid input, not a reading above 100%.
        assert result is None, f"overload {load}/{capacity} returned {result}"
    else:
        assert result == load * 100 // capacity


@given(st.integers(1, 10000))
def test_load_percent_zero_capacity_rejected(load):
    """A capacity of zero must be rejected, never a division by zero."""
    assert load_percent(f"{load} of 0") is None
