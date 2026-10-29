"""Lab 6: application line coverage, including error paths."""
import pytest
from bowling_alley import lane_cost, frame_score, lane_assignment


@pytest.mark.parametrize("args, expected", [
    (("weekday", 1, 1, 0, False), 400),
    (("weekend", 2, 6, 6, True), 1360),
    (("weekday", 2, 4, 2, False), 900),
])
def test_booking_prices(args, expected):
    assert lane_cost(*args) == expected


@pytest.mark.parametrize("args, message", [
    (("holiday", 1, 1, 0, False), "unknown day type"),
    (("weekday", 0, 1, 0, False), "invalid booking"),
    (("weekday", 1, 2, 3, False), "too many shoe rentals"),
])
def test_booking_errors(args, message):
    with pytest.raises(ValueError, match=message):
        lane_cost(*args)


@pytest.mark.parametrize("args, expected", [
    ((10, 0, [10, 10]), 30),
    ((6, 4, [7]), 17),
    ((3, 5, []), 8),
    ((0, 0, []), 0),
])
def test_frame_scores(args, expected):
    assert frame_score(*args) == expected


@pytest.mark.parametrize("args, message", [
    ((-1, 0, []), "invalid roll"),
    ((6, 5, []), "invalid frame"),
])
def test_frame_errors(args, message):
    with pytest.raises(ValueError, match=message):
        frame_score(*args)


@pytest.mark.parametrize("args, expected", [
    ((2, False, 0), "wait"),
    ((2, True, 1), "bumper lane"),
    ((7, False, 2), "two lanes"),
    ((7, False, 1), "wait"),
    ((6, False, 1), "standard lane"),
])
def test_assignments(args, expected):
    assert lane_assignment(*args) == expected
