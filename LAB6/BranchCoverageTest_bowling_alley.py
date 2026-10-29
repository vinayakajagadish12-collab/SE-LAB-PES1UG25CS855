"""Lab 6: both outcomes of each decision and validation boundaries."""
import pytest
from bowling_alley import lane_cost, frame_score, lane_assignment


@pytest.mark.parametrize("args, expected", [
    (("weekday", 1, 1, 0, False), 400),
    (("weekend", 1, 4, 4, False), 800),
    (("weekday", 2, 5, 0, False), 1000),
    (("weekend", 2, 6, 6, True), 1360),
    (("weekday", 1, 1, 1, True), 360),
])
def test_cost_decisions(args, expected):
    assert lane_cost(*args) == expected


@pytest.mark.parametrize("args, message", [
    (("holiday", 1, 1, 0, False), "unknown day type"),
    (("weekday", 0, 1, 0, False), "invalid booking"),
    (("weekday", 1, 0, 0, False), "invalid booking"),
    (("weekday", 1, 7, 0, False), "invalid booking"),
    (("weekday", 1, 2, 3, False), "too many shoe rentals"),
])
def test_each_cost_validation(args, message):
    with pytest.raises(ValueError, match=message):
        lane_cost(*args)


@pytest.mark.parametrize("args, expected", [
    ((10, 0, [4, 5]), 19),
    ((0, 10, [6]), 16),
    ((9, 1, [0]), 10),
    ((0, 0, []), 0),
    ((4, 5, []), 9),
])
def test_frame_decisions(args, expected):
    assert frame_score(*args) == expected


@pytest.mark.parametrize("args, message", [
    ((-1, 0, []), "invalid roll"),
    ((11, 0, []), "invalid roll"),
    ((0, -1, []), "invalid roll"),
    ((9, 2, []), "invalid frame"),
])
def test_each_frame_validation(args, message):
    with pytest.raises(ValueError, match=message):
        frame_score(*args)


@pytest.mark.parametrize("args, expected", [
    ((7, True, 0), "wait"),
    ((7, True, 2), "bumper lane"),
    ((7, False, 2), "two lanes"),
    ((7, False, 1), "wait"),
    ((6, False, 2), "standard lane"),
    ((1, False, 1), "standard lane"),
])
def test_assignment_decisions_and_priority(args, expected):
    assert lane_assignment(*args) == expected
