# src/data_handler.py
from __future__ import annotations
from typing import Dict, List
from datetime import datetime

from .models import User, Ride, RideParticipation


class DataHandler:
    def __init__(self):
        self._users: Dict[str, User] = {}
        self._rides: Dict[int, Ride] = {}
        self._seq = 1                                      # Autoincrement para Ride.id

    # ------------------------ Usuarios --------------------------------------------
    def create_user(self, alias: str, name: str, car_plate: str | None = None) -> User:
        if alias in self._users:
            raise ValueError("Alias already exists")
        user = User(alias=alias, name=name, car_plate=car_plate)
        self._users[alias] = user
        return user

    def list_users(self) -> List[User]:
        return list(self._users.values())

    def get_user(self, alias: str) -> User | None:
        return self._users.get(alias)

    # ------------------------ Rides ------------------------------------------------
    def create_ride(
        self,
        driver_alias: str,
        ride_date_and_time: datetime,
        final_address: str,
        allowed_spaces: int,
    ) -> Ride:
        driver = self.get_user(driver_alias)
        if driver is None:
            raise LookupError("Driver not found")
        ride = Ride(
            id=self._seq,
            ride_date_and_time=ride_date_and_time,
            final_address=final_address,
            allowed_spaces=allowed_spaces,
            ride_driver=driver,
        )
        self._seq += 1
        self._rides[ride.id] = ride
        return ride

    def user_rides(self, alias: str) -> List[Ride]:
        return [r for r in self._rides.values() if r.ride_driver.alias == alias]

    def get_ride(self, ride_id: int) -> Ride | None:
        return self._rides.get(ride_id)

    # ------------------------ Solicitudes -----------------------------------------
    def request_to_join(
        self, ride_id: int, participant_alias: str, destination: str, spaces: int
    ):
        ride = self._ensure_ride_ready(ride_id)
        if ride.find_participation(participant_alias):
            raise ValueError("Duplicate request")
        participant = self.get_user(participant_alias)
        if participant is None:
            raise LookupError("Participant not found")
        rp = RideParticipation(
            participant=participant,
            destination=destination,
            occupied_spaces=spaces,
        )
        ride.participants.append(rp)
        participant.rides.append(rp)
        return rp

    def accept(self, ride_id: int, participant_alias: str):
        ride = self._ensure_ride_ready(ride_id)
        rp = ride.find_participation(participant_alias) or self._notfound()
        if rp.status != "waiting":
            raise ValueError("Already processed")
        if ride.free_spaces < rp.occupied_spaces:
            raise ValueError("No free spaces")
        rp.set_status("confirmed")
        rp.confirmation = datetime.now()

    def reject(self, ride_id: int, participant_alias: str):
        ride = self._ensure_ride_ready(ride_id)
        rp = ride.find_participation(participant_alias) or self._notfound()
        if rp.status != "waiting":
            raise ValueError("Already processed")
        rp.set_status("rejected")

    # ------------------------ Ciclo de vida ---------------------------------------
    def start(self, ride_id: int):
        ride = self._ensure_ride_ready(ride_id)
        # Mark present & missing
        for rp in ride.participants:
            if rp.status == "confirmed":
                rp.set_status("inprogress")
            elif rp.status in ("waiting", "rejected"):
                rp.set_status("missing")
        ride.status = "inprogress"

    def unload(self, ride_id: int, participant_alias: str):
        ride = self.get_ride(ride_id) or self._notfound()
        if ride.status != "inprogress":
            raise ValueError("Ride not in progress")
        rp = ride.find_participation(participant_alias) or self._notfound()
        if rp.status != "inprogress":
            raise ValueError("Participant not in ride")
        rp.set_status("done")

    def end(self, ride_id: int):
        ride = self.get_ride(ride_id) or self._notfound()
        if ride.status != "inprogress":
            raise ValueError("Ride not in progress")
        for rp in ride.participants:
            if rp.status == "inprogress":       # Se olvidó marcar bajada
                rp.set_status("notmarked")
        ride.status = "done"

    # ------------------------ Utils ------------------------------------------------
    def _ensure_ride_ready(self, ride_id: int) -> Ride:
        ride = self.get_ride(ride_id) or self._notfound()
        if ride.status != "ready":
            raise ValueError("Ride already started or finished")
        return ride

    @staticmethod
    def _notfound():
        raise LookupError("Not found")
