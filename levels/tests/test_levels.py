import datetime

from django.test import Client, TestCase
from django.utils import timezone
from django.urls import reverse
from rest_framework import status

from devices.models import Device, RecordingType
from levels.models import User
from levels.tests.utils import (
    get_dummy_user,
    get_dummy_device,
    get_dummy_recording_type,
    get_dummy_glucose_level,
)


class GlucoseLevelTestCase(TestCase):
    def setUp(self) -> None:
        self.user: User = get_dummy_user()
        self.second_user: User = get_dummy_user()
        self.device: Device = get_dummy_device()
        self.rec_type: RecordingType = get_dummy_recording_type(1)
        self.client = Client()

        for i in range(1, 6):
            get_dummy_glucose_level(
                self.user,
                self.device,
                datetime.datetime(2022, 2, i, tzinfo=timezone.utc),
                self.rec_type,
                i,
            )
            get_dummy_glucose_level(
                self.second_user,
                self.device,
                datetime.datetime(2022, 2, i, tzinfo=timezone.utc),
                self.rec_type,
                i,
            )
        self.list_url = reverse('levels:levels-list')
        # data to test filtering
        get_dummy_recording_type(2)

    def test_list_all(self) -> None:
        result = self.client.get(self.list_url)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        data = result.json()
        self.assertEqual(data['count'], 10)

    def test_list_invalid_user(self) -> None:
        result = self.client.get(
            self.list_url,
            data={
                'user_id': 'qwertyuiolp',
            },
        )
        data = result.json()
        self.assertEqual(data['count'], 0)

    def test_list_filter_user(self) -> None:
        result = self.client.get(
            self.list_url, data={'user_id': self.user.name}
        )
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        data = result.json()
        self.assertEqual(data['count'], 5)

    def test_list_start_stop(self) -> None:
        result = self.client.get(
            self.list_url,
            data={
                'user_id': self.user.name,
                'start': datetime.datetime(2022, 2, 2),
                'stop': datetime.datetime(2022, 2, 4),
            },
        )
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        data = result.json()
        self.assertEqual(data['count'], 3)

    def test_list_order_date_asc(self) -> None:
        result = self.client.get(
            self.list_url,
            data={
                'user_id': self.user.name,
                'ordering': 'device_timestamp',
            },
        )
        data = result.json()
        self.assertGreater(
            data['results'][1]['device_timestamp'],
            data['results'][0]['device_timestamp'],
        )

    def test_list_order_date_desc(self) -> None:
        result = self.client.get(
            self.list_url,
            data={
                'user_id': self.user.name,
                'ordering': '-device_timestamp',
            },
        )
        data = result.json()
        self.assertGreater(
            data['results'][0]['device_timestamp'],
            data['results'][1]['device_timestamp'],
        )

    def test_list_pagination(self) -> None:
        result = self.client.get(
            self.list_url,
            data={'page_size': 2, 'page': 5},
        )
        data = result.json()
        self.assertEqual(data['count'], 10)
        self.assertEqual(len(data['results']), 2)
        self.assertIsNone(data['next'])

    def test_list_pagination_invalid_page(self) -> None:
        result = self.client.get(
            self.list_url,
            data={'page_size': 2, 'page': 15},
        )
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)
