# tests/test_rides.py
import pytest
from datetime import datetime, timedelta
from src.data_handler import DataHandler


def setup():
    """Repositorio y datos base para cada test."""
    db = DataHandler()
    db.create_user("driver", "Conductor Uno", car_plate="ABC-123")
    db.create_user("p1", "Passenger Uno")
    db.create_user("p2", "Passenger Dos")
    return db


# ----------Caso de éxito ---------------------------------------------------------
def test_full_flow_success():
    """
    Flujo feliz: crear ride, p1 pide, driver acepta,
    se inicia el ride, p1 baja y driver termina.
    """
    db = setup()
    ride = db.create_ride("driver", datetime.now() + timedelta(hours=1), "Destino", 2)
    db.request_to_join(ride.id, "p1", "Destino P1", 1)
    db.accept(ride.id, "p1")
    db.start(ride.id)
    db.unload(ride.id, "p1")
    db.end(ride.id)

    assert ride.status == "done"
    rp = ride.find_participation("p1")
    assert rp.status == "done"


# ----------Errores ---------------------------------------------------------------
def test_join_after_started():
    """Error: solicitar unirse después de iniciado el ride."""
    db = setup()
    ride = db.create_ride("driver", datetime.now(), "X", 1)
    db.start(ride.id)
    with pytest.raises(ValueError):
        db.request_to_join(ride.id, "p1", "Y", 1)


def test_accept_without_seats():
    """Error: aceptar cuando no hay asientos libres."""
    db = setup()
    ride = db.create_ride("driver", datetime.now(), "X", 1)
    db.request_to_join(ride.id, "p1", "Y", 1)
    db.accept(ride.id, "p1")
    db.request_to_join(ride.id, "p2", "Z", 1)
    with pytest.raises(ValueError):
        db.accept(ride.id, "p2")


def test_duplicate_request():
    """Error: mismo usuario envía 2 solicitudes al mismo ride."""
    db = setup()
    ride = db.create_ride("driver", datetime.now(), "X", 2)
    db.request_to_join(ride.id, "p1", "Y", 1)
    with pytest.raises(ValueError):
        db.request_to_join(ride.id, "p1", "Y", 1)
