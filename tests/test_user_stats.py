# tests/test_user_stats.py
from src.models import User, RideParticipation

def test_ride_stats_summary():
    u = User(alias="ana", name="Ana")
    for st in ["done", "missing", "notmarked", "rejected", "confirmed"]:
        u.rides.append(RideParticipation(participant=u, destination="X",
                                         occupied_spaces=1, status=st))
    assert u.ride_stats() == {
        "previousRidesTotal": 5,
        "previousRidesCompleted": 1,
        "previousRidesMissing": 1,
        "previousRidesNotMarked": 1,
        "previousRidesRejected": 1,
    }
