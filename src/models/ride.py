# src/models/ride.py
from __future__ import annotations
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class Ride(BaseModel):
    id: int
    ride_date_and_time: datetime
    final_address: str
    allowed_spaces: int = Field(..., gt=0)
    ride_driver: "User"
    status: str = Field(default="ready", regex=r"^(ready|inprogress|done)$")
    participants: List["RideParticipation"] = []

    # --------------------------------- Lógica --------------------------------------
    @property
    def occupied(self) -> int:
        """Asientos confirmados o en progreso."""
        return sum(
            rp.occupied_spaces
            for rp in self.participants
            if rp.status in ("confirmed", "inprogress", "done")
        )

    @property
    def free_spaces(self) -> int:
        return self.allowed_spaces - self.occupied

    def find_participation(self, alias: str):
        for rp in self.participants:
            if rp.participant.alias == alias:
                return rp
        return None
