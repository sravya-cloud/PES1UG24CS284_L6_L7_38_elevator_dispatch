import pytest

from elevator_dispatch import next_direction, door_action, pick_elevator


# next_direction: current direction is up
def test_up_direction_with_request_above():
    assert next_direction(3, "up", [5, 1]) == "up"


def test_up_direction_with_only_request_below():
    assert next_direction(3, "up", [1]) == "down"


def test_up_direction_with_no_requests():
    assert next_direction(3, "up", []) == "idle"


# next_direction: current direction is down
def test_down_direction_with_request_below():
    assert next_direction(3, "down", [1, 5]) == "down"


def test_down_direction_with_only_request_above():
    assert next_direction(3, "down", [5]) == "up"


def test_down_direction_with_no_requests():
    assert next_direction(3, "down", []) == "idle"


# next_direction: idle/other direction
def test_idle_direction_with_request_above():
    assert next_direction(3, "idle", [5]) == "up"


def test_idle_direction_with_request_below():
    assert next_direction(3, "idle", [1]) == "down"


def test_idle_direction_with_no_requests():
    assert next_direction(3, "idle", []) == "idle"


# door_action priority and outcomes
def test_emergency_has_highest_priority():
    assert door_action(700, True, True) == "hold_open"


def test_overload_action():
    assert door_action(631, False, False) == "overload"


def test_blocked_door_reopens():
    assert door_action(500, True, False) == "reopen"


def test_normal_door_closes():
    assert door_action(500, False, False) == "close"


def test_exact_capacity_is_not_overload():
    assert door_action(630, False, False) == "close"


# pick_elevator selection
def test_pick_elevator_returns_none_for_empty_list():
    assert pick_elevator([], 4) is None


def test_pick_elevator_selects_nearest_idle_car():
    cars = [("A", 1, True), ("B", 5, True)]
    assert pick_elevator(cars, 4) == "B"


def test_pick_elevator_applies_busy_car_penalty():
    cars = [("A", 4, False), ("B", 8, True)]
    assert pick_elevator(cars, 4) == "B"


def test_pick_elevator_keeps_first_car_on_equal_gap():
    cars = [("A", 2, True), ("B", 6, True)]
    assert pick_elevator(cars, 4) == "A"


def test_pick_elevator_handles_single_car():
    assert pick_elevator([("A", 10, True)], 2) == "A"
