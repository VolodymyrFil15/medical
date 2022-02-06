import string
import random
import uuid

from devices.models import Device, RecordingType
from levels.models import GlucoseLevel, User


def get_random_name(length: int) -> str:
    return ''.join(
        random.choice(string.ascii_uppercase) for _ in range(length)
    )


def get_dummy_user() -> User:
    name = get_random_name(3)
    user = User(name=name)
    user.save()
    return user


def get_dummy_device() -> Device:
    _uuid = uuid.uuid1(random.randint(0, 281474976710655))
    device = Device(serial_number=_uuid, name=get_random_name(5))
    device.save()
    return device


def get_dummy_recording_type(_id: int) -> RecordingType:
    rec_type = RecordingType(id=_id)
    rec_type.save()
    return rec_type


def get_dummy_glucose_level(
    user,
    device,
    created_date,
    recording_type,
    glucose_value_history,
) -> GlucoseLevel:

    level = GlucoseLevel(
        created_by=user,
        device=device,
        device_timestamp=created_date,
        recording_type=recording_type,
        glucose_value_history=glucose_value_history,
    )
    level.save()
    return level
