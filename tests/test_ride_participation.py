import pytest
from src.models import User, RideParticipation

def test_invalid_status_change():
    rp = RideParticipation(participant=User(alias="bob", name="Bob"),
                           destination="Y", occupied_spaces=1)
    with pytest.raises(ValueError):
        rp.set_status("fly")
