
import json

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import User
from core.tests.pytests.data_generators import SimpleTestDataGenerator


class TestAppointmentsProcessors(APITestCase, SimpleTestDataGenerator):

    def get_token(self):
        url = reverse('token_obtain_pair')
        u = User.objects.create_user(username='user', email='user@foo.com', password='pass')
        u.is_active = True
        u.save()
        resp = self.client.post(url, {'username': 'user', 'password': 'pass'}, format='json')
        return resp.data['access']

    def test_api_jwt(self):
        url = reverse('token_obtain_pair')
        u = User.objects.create_user(username='user', email='user@foo.com', password='pass')
        u.is_active = False
        u.save()

        resp = self.client.post(url, {'email': 'user@foo.com', 'password': 'pass'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        u.is_active = True
        u.save()

        resp = self.client.post(url, {'username': 'user', 'password': 'pass'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in resp.data)

    @pytest.mark.django_db
    def test_MakeAppointment_POST(self):
        self.generate_data()
        token = self.get_token()

        request = {
            "time": "2020-08-05 14:00",
            "workman_id": 1
        }
        view_path = reverse("make_appointment")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.post(view_path, json.dumps(request),
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                    content_type='application/json')

        is_error, _ = response.data['is_error'], response.data['info']
        self.assertFalse(is_error)

    @pytest.mark.django_db
    def test_MakeAppointment_POST_on_occupied_time(self):
        self.generate_data()
        token = self.get_token()

        request = {
            "time": "2020-08-05 13:00",
            "workman_id": 1
        }
        view_path = reverse("make_appointment")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.post(view_path, json.dumps(request),
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                    content_type='application/json')

        is_error, _ = response.data['is_error'], response.data['info']
        self.assertTrue(is_error)

    @pytest.mark.django_db
    def test_CheckRepairShopWorkload_GET(self):
        self.generate_data()
        token = self.get_token()

        request = {
            "date": "2020-08-05",
            "workman_id": 1
        }
        view_path = reverse("check_workload")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(view_path, data=request)

        is_error, info = response.data['is_error'], response.data['info']
        self.assertFalse(is_error)
        self.assertTrue("75" in info)

    @pytest.mark.django_db
    def test_GetAvailableAppointmentTime_GET(self):
        self.generate_data()
        token = self.get_token()

        request = {
            "date": "2020-08-05",
            "workman_id": 1
        }
        view_path = reverse("get_available_appointment_time")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(view_path, data=request)

        is_error, info = response.data['is_error'], response.data['info']
        self.assertFalse(is_error)
        self.assertTrue("2020/08/05 14:00" in info)
        self.assertTrue("2020/08/05 15:00" in info)

    @pytest.mark.django_db
    def test_MakeAppointment_GET(self):
        self.generate_data()
        token = self.get_token()

        request = {
            "time": "2020-01-01 09:00",
            "workman_id": 1
        }
        view_path = reverse("make_appointment")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(view_path, data=request)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @pytest.mark.django_db
    def test_CheckRepairShopWorkload_POST(self):
        self.generate_data()
        token = self.get_token()

        request = {
            "time": "2020-01-01 09:00",
            "workman_id": 1
        }
        view_path = reverse("check_workload")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.post(view_path, json.dumps(request),
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @pytest.mark.django_db
    def test_GetAvailableAppointmentTime_POST(self):
        self.generate_data()
        token = self.get_token()

        request = {
            "time": "2020-01-01 09:00",
            "workman_id": 1
        }
        view_path = reverse("get_available_appointment_time")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.post(view_path, json.dumps(request),
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
