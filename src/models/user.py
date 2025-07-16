# src/models/user.py
from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field


class User(BaseModel):
    alias: str = Field(..., regex=r"^[a-zA-Z0-9_]+$")
    name: str
    car_plate: Optional[str] = None    # Null cuando es solo participante
    rides: List["RideParticipation"] = []

    # ----- Estadísticas históricas -------------------------------------------------
    def ride_stats(self) -> dict:
        total = len(self.rides)
        completed = sum(r.status == "done" for r in self.rides)
        missing = sum(r.status == "missing" for r in self.rides)
        notmarked = sum(r.status == "notmarked" for r in self.rides)
        rejected = sum(r.status == "rejected" for r in self.rides)
        return dict(
            previousRidesTotal=total,
            previousRidesCompleted=completed,
            previousRidesMissing=missing,
            previousRidesNotMarked=notmarked,
            previousRidesRejected=rejected,
        )
