"""
Elevator Dispatch - hardened against malformed input (Lab 7).

Every public function follows the same contract:
  * it accepts anything at all without raising,
  * it returns a validated result on good input,
  * it returns None on input it cannot make sense of.

Returning None rather than raising keeps the caller in control and means
no user-supplied string can ever take the dispatcher down.
"""

import re

# Floors the building actually has. Anything outside this is a bad request.
MIN_FLOOR = -10
MAX_FLOOR = 200

# Longest input accepted, so a huge paste cannot stall the parser.
MAX_INPUT_LENGTH = 1000

# Most floors accepted in one journey.
MAX_FLOORS_PER_TRIP = 500

# Strict integer: optional sign, then ASCII digits only. Deliberately
# stricter than int(), which also accepts underscores ("1_0"), surrounding
# whitespace and non-ASCII digits.
_INTEGER_PATTERN = re.compile(r"[+-]?[0-9]+")


def _clean_text(value):
    """Return value as a usable string, or None if it is not one."""
    if not isinstance(value, str):
        return None
    if len(value) > MAX_INPUT_LENGTH:
        return None
    return value.strip()


def _to_int(token):
    """Convert a token to int using the strict pattern, or None."""
    if not isinstance(token, str):
        return None
    token = token.strip()
    if not _INTEGER_PATTERN.fullmatch(token):
        return None
    return int(token)


def _to_floor(token):
    """Convert a token to a floor inside the building, or None."""
    floor = _to_int(token)
    if floor is None or not (MIN_FLOOR <= floor <= MAX_FLOOR):
        return None
    return floor


def parse_request(text):
    """
    Parse a request written as 'FROM->TO', e.g. '5->9'.

    Returns (start, end) as a tuple of ints within the building's floor
    range, or None if the request is malformed.
    """
    text = _clean_text(text)
    if not text:
        return None

    parts = text.split("->")
    if len(parts) != 2:
        # Covers both a missing arrow and chained requests like '1->2->3'.
        return None

    start = _to_floor(parts[0])
    end = _to_floor(parts[1])
    if start is None or end is None:
        return None

    return start, end


def total_travel(floors_csv):
    """
    Total distance travelled across a comma-separated list of floors,
    e.g. '1,5,3,9'.

    Returns a non-negative int, or None if the list is malformed.
    A single floor is valid and means no travel.
    """
    floors_csv = _clean_text(floors_csv)
    if not floors_csv:
        return None

    tokens = floors_csv.split(",")
    if len(tokens) > MAX_FLOORS_PER_TRIP:
        return None

    floors = []
    for token in tokens:
        floor = _to_floor(token)
        if floor is None:
            # Catches empty entries from '1,,3' as well as '1,abc,3'.
            return None
        floors.append(floor)

    return sum(abs(floors[i + 1] - floors[i]) for i in range(len(floors) - 1))


def load_percent(text):
    """
    Current car load as a percentage, written as 'X of Y', e.g. '450 of 630'.

    Returns an int between 0 and 100, or None if the reading is malformed,
    the capacity is not positive, the load is negative, or the load exceeds
    the capacity.
    """
    text = _clean_text(text)
    if not text:
        return None

    parts = text.split(" of ")
    if len(parts) != 2:
        return None

    load = _to_int(parts[0])
    capacity = _to_int(parts[1])
    if load is None or capacity is None:
        return None

    if capacity <= 0:
        # A capacity of zero would be a division by zero.
        return None
    if load < 0:
        return None
    if load > capacity:
        # An overloaded car is a faulty reading, not a figure above 100%.
        return None

    return load * 100 // capacity


def _report(label, value):
    """Print a result, or a clear message when the input was rejected."""
    if value is None:
        print(f"{label}: invalid input - request ignored")
    else:
        print(f"{label}: {value}")


def main():
    print("==== Running parse_request ====")
    user_input = input("Enter a request as FROM->TO (e.g. 5->9): ")
    _report("From and To", parse_request(user_input))

    print("\n==== Running total_travel ====")
    user_input = input("Enter floors visited as CSV (e.g. 1,5,3,9): ")
    _report("Floors Travelled", total_travel(user_input))

    print("\n==== Running load_percent ====")
    user_input = input("Enter load as 'X of Y' (e.g. 450 of 630): ")
    _report("Load Percent", load_percent(user_input))


if __name__ == "__main__":
    main()
