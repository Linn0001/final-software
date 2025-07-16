from .user import User               # noqa
from .ride_participation import RideParticipation  # noqa
from .ride import Ride               # noqa

User.model_rebuild()
RideParticipation.model_rebuild()
Ride.model_rebuild()