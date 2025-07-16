# src/controller.py
from fastapi import FastAPI, HTTPException, status, Body
from datetime import datetime
from typing import List

from .data_handler import DataHandler

app = FastAPI(
    title="UTEC Ride API",
    description="API del examen final – IS 1 (2025‑1)",
    version="1.0.0",
)

db = DataHandler()

# ---------------------------Usuarios --------------------------------------------
@app.get("/usuarios", response_model=List[dict])
def list_users():
    return [u.dict(exclude={"rides"}) for u in db.list_users()]


@app.get("/usuarios/{alias}")
def get_user(alias: str):
    user = db.get_user(alias)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


# ---------------------------Rides de un usuario ---------------------------------
@app.get("/usuarios/{alias}/rides")
def rides_by_user(alias: str):
    if not db.get_user(alias):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db.user_rides(alias)


@app.post("/usuarios/{alias}/rides")
def create_ride(alias: str, datetime_iso: str, destino: str, espacios: int):
    try:
        date = datetime.fromisoformat(datetime_iso)
        ride = db.create_ride(alias, date, destino, espacios)
        return ride
    except LookupError:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")


@app.get("/usuarios/{alias}/rides/{ride_id}")
def ride_detail(alias: str, ride_id: int):
    ride = db.get_ride(ride_id)
    if not ride or ride.ride_driver.alias != alias:
        raise HTTPException(status_code=404, detail="No encontrado")
    # Embellecemos la respuesta según el ejemplo del enunciado
    enriched = ride.dict()
    enriched["participants"] = [
        {
            "confirmation": rp.confirmation,
            "participant": {
                **rp.participant.dict(exclude={"rides"}),
                **rp.participant.ride_stats(),
            },
            "destination": rp.destination,
            "occupiedSpaces": rp.occupied_spaces,
            "status": rp.status,
        }
        for rp in ride.participants
    ]
    return {"ride": enriched}


# ---------------------------Acciones sobre rides --------------------------------
@app.post("/usuarios/{alias}/rides/{ride_id}/requestToJoin/{part_alias}")
def request_join(alias: str, ride_id: int, part_alias: str, destino: str, espacios: int):
    _assert_driver(alias, ride_id)
    try:
        rp = db.request_to_join(ride_id, part_alias, destino, espacios)
        return rp
    except LookupError:
        raise HTTPException(status_code=404, detail="Participante o ride no encontrado")
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.post("/usuarios/{alias}/rides/{ride_id}/accept/{part_alias}")
def accept(alias: str, ride_id: int, part_alias: str):
    _assert_driver(alias, ride_id)
    try:
        db.accept(ride_id, part_alias)
    except (LookupError, ValueError) as e:
        raise HTTPException(_http(e), detail=str(e))


@app.post("/usuarios/{alias}/rides/{ride_id}/reject/{part_alias}")
def reject(alias: str, ride_id: int, part_alias: str):
    _assert_driver(alias, ride_id)
    try:
        db.reject(ride_id, part_alias)
    except (LookupError, ValueError) as e:
        raise HTTPException(_http(e), detail=str(e))


@app.post("/usuarios/{alias}/rides/{ride_id}/start")
def start(alias: str, ride_id: int):
    _assert_driver(alias, ride_id)
    try:
        db.start(ride_id)
    except (LookupError, ValueError) as e:
        raise HTTPException(_http(e), detail=str(e))


@app.post("/usuarios/{alias}/rides/{ride_id}/end")
def end(alias: str, ride_id: int):
    _assert_driver(alias, ride_id)
    try:
        db.end(ride_id)
    except (LookupError, ValueError) as e:
        raise HTTPException(_http(e), detail=str(e))


@app.post("/usuarios/{alias}/rides/{ride_id}/unloadParticipant")
def unload(
    alias: str,
    ride_id: int,
    part_alias: str | None = None,
    body: dict | None = Body(None)
):
    # Permite:
    #   - /.../unloadParticipant?part_alias=p1
    #   - body {"alias": "p1"}
    if part_alias is None and body and "alias" in body:
        part_alias = body["alias"]
    if part_alias is None:
        raise HTTPException(422, "Debe indicar 'alias' del participante")
    _assert_driver(alias, ride_id)
    try:
        db.unload(ride_id, part_alias)
    except (LookupError, ValueError) as e:
        raise HTTPException(_http(e), detail=str(e))


# ---------------------------Utilities-------------------------------------------
def _assert_driver(alias: str, ride_id: int):
    ride = db.get_ride(ride_id)
    if not ride or ride.ride_driver.alias != alias:
        raise HTTPException(status_code=404, detail="Ride no encontrado")


def _http(exc: Exception) -> int:
    return 404 if isinstance(exc, LookupError) else 422

@app.get("/rides/active")
def list_active_rides():
    """Devuelve todos los rides con status 'ready' o 'inprogress'."""
    return [
        r for r in db._rides.values()     # acceso directo al store in‑memory
        if r.status in ("ready", "inprogress")
    ]
