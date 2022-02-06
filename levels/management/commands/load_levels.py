import csv
import datetime
import logging
import sys

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils import timezone

from devices.models import Device, RecordingType
from levels.models import User, GlucoseLevel

logger = logging.getLogger(__name__)


def validate_heading(row):
    if not isinstance(row, list) or len(row) < 5:
        logger.error('Invalid heading format')
        exit(1)

    if row[0] != 'Glukose-Werte':
        logger.error('Please provide valid glucose levels file')
        exit(1)


def get_user(user_name):
    user, _ = User.objects.get_or_create(name=user_name)
    return user


def get_device(serial_number, name):
    device, _ = Device.objects.get_or_create(
        serial_number=serial_number, name=name
    )
    return device


def get_recording_type(_id):
    recording_type, _ = RecordingType.objects.get_or_create(id=_id)
    return recording_type


def process_item(row, user, devices, recording_types):
    serial_number = row[1]
    if serial_number in devices:
        device = devices[serial_number]
    else:
        device = get_device(serial_number, row[0])
        devices[serial_number] = device

    recording_type_id = row[3]
    if recording_type_id in recording_types:
        recording_type = recording_types[recording_type_id]
    else:
        recording_type = get_recording_type(recording_type_id)
        recording_types[recording_type_id] = recording_type

    datetime_created = datetime.datetime.strptime(row[2], '%d-%m-%Y %H:%M')
    datetime_created = datetime_created.replace(tzinfo=timezone.utc)

    level = GlucoseLevel(
        created_by=user,
        device=device,
        device_timestamp=datetime_created,
        recording_type=recording_type,
        glucose_value_history=int(row[4]) if row[4] else None,
        glucose_scan=int(row[5]) if row[5] else None,
        rapid_acting_insulin=row[6],
        rapid_acting_insulin_units=int(row[7]) if row[7] else None,
        nutritional_data=row[8],
        carbohydrates_grams=int(row[9]) if row[9] else None,
        carbohydrates_servings=int(row[10]) if row[10] else None,
        depot_insulin=row[11],
        depot_insulin_units=int(row[12]) if row[12] else None,
        notes=row[13],
        glucose_test_strips=int(row[14]) if row[14] else None,
        ketone=int(row[15]) if row[15] else None,
        meal_insulin=int(row[16]) if row[16] else None,
        correction_insulin=int(row[17]) if row[17] else None,
        user_insulin_changes=int(row[18]) if row[18] else None,
    )
    try:
        level.save()
        return True
    except IntegrityError:
        return False


class Command(BaseCommand):
    help = 'load info from file'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--file', help='input file')

    def handle(self, *args, **options):
        file = options.get('file')
        if not file:
            logger.error('File parameter is required')
            sys.exit(1)

        devices, recording_types = {}, {}

        created = 0
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            heading = next(reader)
            validate_heading(heading)

            user_id = get_user(heading[4])

            # Skip blank line and column's names
            while True:
                row = next(reader)
                if row and row[0] == 'Gerät':
                    break

            for row in reader:
                success = process_item(row, user_id, devices, recording_types)
                if success:
                    created += 1

        logger.info('Created %s items', created)
