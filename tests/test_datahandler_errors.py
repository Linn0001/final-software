import pytest, datetime
from src.data_handler import DataHandler

def test_duplicate_alias_error():
    db = DataHandler()
    db.create_user("dup", "Uno")
    with pytest.raises(ValueError):
        db.create_user("dup", "Dos")

def test_accept_no_space_error():
    db = DataHandler()
    db.create_user("drv", "Driver", car_plate="AAA")
    db.create_user("p1", "Pas 1")
    db.create_user("p2", "Pas 2")
    ride = db.create_ride("drv", datetime.datetime.now(), "X", 1)
    db.request_to_join(ride.id, "p1", "X", 1)
    db.accept(ride.id, "p1")
    db.request_to_join(ride.id, "p2", "X", 1)
    with pytest.raises(ValueError):
        db.accept(ride.id, "p2")

def test_request_to_join_nonexistent_ride():
    db = DataHandler()
    db.create_user("u1", "Uno")
    with pytest.raises(LookupError):
        db.request_to_join(99, "u1", "X", 1)    # ride 99 no existe


def test_start_already_started_ride():
    db = DataHandler()
    db.create_user("d", "Driver", car_plate="XYZ-987")
    ride = db.create_ride("d", datetime.datetime.now(), "Y", 1)
    db.start(ride.id)
    with pytest.raises(ValueError):
        db.start(ride.id)                       # intentar iniciar 2 veces