from elevator_dispatch import next_direction, door_action, pick_elevator


# Exercise both outcomes of each direction decision.
def test_next_direction_up_all_branches():
    assert next_direction(5, "up", [8]) == "up"       # above exists
    assert next_direction(5, "up", [2]) == "down"     # no above, below exists
    assert next_direction(5, "up", []) == "idle"      # neither exists


def test_next_direction_down_all_branches():
    assert next_direction(5, "down", [2]) == "down"   # below exists
    assert next_direction(5, "down", [8]) == "up"     # no below, above exists
    assert next_direction(5, "down", []) == "idle"


def test_next_direction_idle_all_branches():
    assert next_direction(5, "idle", [8]) == "up"
    assert next_direction(5, "idle", [2]) == "down"
    assert next_direction(5, "idle", []) == "idle"


# Exercise all return branches and priority decisions.
def test_door_action_all_branches():
    assert door_action(100, False, True) == "hold_open"
    assert door_action(631, False, False) == "overload"
    assert door_action(630, True, False) == "reopen"
    assert door_action(630, False, False) == "close"


# Exercise empty/non-empty loop, first item, later items, and tie handling.
def test_pick_elevator_all_branches():
    assert pick_elevator([], 3) is None
    assert pick_elevator([("A", 3, True)], 3) == "A"
    assert pick_elevator([("A", 3, False), ("B", 7, True)], 3) == "B"
    assert pick_elevator([("A", 1, True), ("B", 5, True)], 3) == "A"
