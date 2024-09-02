from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tracker.models import Habit
from users.models import User


# {
#     "name": "Тестовая привычка",
#     "place": "В тесте",
#     "action": "Протестировать",
#     "first_time_to_do": "2024-09-02T19:10:04.709123+03:00",
#     "reward": "тест пройден",
#     "relation_habit": null,
#     "is_pleasant": false,
#     "periodicity": 1,
#     "duration": "02:00",
#     "is_public": false,
#     "is_active": false
# }
#
# data = {
#                 "name": "Тестовая привычка",
#                 "place": "В тесте",
#                 "action": "Протестировать",
#                 "first_time_to_do": "2024-09-02T19:10:04.709123+03:00",
#                 "reward": "тест пройден",
#                 "relation_habit": '',
#                 "is_pleasant": False,
#                 "periodicity": 1,
#                 "duration": "02:00",
#                 "is_public": False,
#                 "is_active": False
#             }

class HabitTestCaseIsOwner(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="owner@owner.com")
        self.habit = Habit.objects.create(
            owner=self.user,
            name="Тестовая привычка для просмотра и изменения", place="В тесте",
            action="Протестировать",
            first_time_to_do="2024-09-02T19:10:04.709123+03:00",
            next_time_to_do="2024-09-02T19:10:04.709123+03:00",
            reward="тест пройден", is_pleasant=False, periodicity=1,
            duration="02:00", is_public=False, is_active=False
        )
        self.data = {
            "name": "Тестовая привычка",
            "place": "В тесте",
            "action": "Протестировать",
            "first_time_to_do": "2024-09-02T19:10:04.709123+03:00",
            "next_time_to_do": "2024-09-02T19:10:04.709123+03:00",
            "reward": "Тест пройден",
            "relation_habit": '',
            "is_pleasant": False,
            "periodicity": 1,
            "duration": "02:00",
            "is_public": False,
            "is_active": True
        }
        self.client.force_authenticate(user=self.user)

    def test_habit_create(self):
        url = reverse("tracker:habit_create")
        response = self.client.post(url, self.data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json(), {
                "name": "Тестовая привычка",
                "place": "В тесте",
                "action": "Протестировать",
                "first_time_to_do": "2024-09-02T19:10:04.709123+03:00",
                "reward": "Тест пройден",
                "relation_habit": None,
                "is_pleasant": False,
                "periodicity": 1,
                "duration": "02:00",
                "is_public": False,
                "is_active": False
            }
        )
        self.assertEqual(
            Habit.objects.all().count(), 2
        )

    def test_lesson_update(self):
        url = reverse("tracker:habit_update", args=(self.habit.pk,))
        response = self.client.patch(url, self.data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            Habit.objects.get(pk=self.habit.pk).name, "Тестовая привычка"
        )

    def test_habit_delete(self):
        url = reverse("tracker:habit_delete", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Habit.objects.all().count(), 0
        )

    def test_habit_list(self):
        url = reverse("tracker:habit_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                 'name': 'Тестовая привычка для просмотра и изменения',
                 'place': 'В тесте',
                 'action': 'Протестировать',
                 'first_time_to_do': '2024-09-02T19:10:04.709123+03:00',
                 'reward': 'тест пройден',
                 'relation_habit': None,
                 'is_pleasant': False,
                 'periodicity': 1,
                 'duration': '02:00',
                 'is_public': False,
                 'is_active': False
                },
            ]
        }
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )


class HabitTestCaseNotOwner(APITestCase):

    def setUp(self):
        self.owner = User.objects.create(email="owner@owner.com")
        self.user = User.objects.create(email="user@user.com")
        self.habit = Habit.objects.create(
            owner=self.owner,
            name="Тестовая привычка для просмотра и изменения", place="В тесте",
            action="Протестировать",
            first_time_to_do="2024-09-02T19:10:04.709123+03:00",
            next_time_to_do="2024-09-02T19:10:04.709123+03:00",
            reward="тест пройден", is_pleasant=False, periodicity=1,
            duration="02:00", is_public=False, is_active=False
        )
        self.data = {
            "name": "Тестовая привычка",
            "place": "В тесте",
            "action": "Протестировать",
            "first_time_to_do": "2024-09-02T19:10:04.709123+03:00",
            "next_time_to_do": "2024-09-02T19:10:04.709123+03:00",
            "reward": "Тест пройден",
            "relation_habit": '',
            "is_pleasant": False,
            "periodicity": 1,
            "duration": "02:00",
            "is_public": False,
            "is_active": True
        }
        self.client.force_authenticate(user=self.user)

    def test_lesson_update(self):
        url = reverse("tracker:habit_update", args=(self.habit.pk,))
        response = self.client.patch(url, self.data)
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )
        self.assertEqual(
            Habit.objects.get(pk=self.habit.pk).name, "Тестовая привычка для просмотра и изменения"
        )

    def test_habit_delete(self):
        url = reverse("tracker:habit_delete", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )
        self.assertEqual(
            Habit.objects.all().count(), 1
        )

    def test_habit_list(self):
        url = reverse("tracker:habit_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 0,
            "next": None,
            "previous": None,
            "results": []
        }
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )


class HabitTestCaseIsAnonymous(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="owner@owner.com")
        self.habit = Habit.objects.create(
            owner=self.user,
            name="Тестовая привычка для просмотра и изменения", place="В тесте",
            action="Протестировать",
            first_time_to_do="2024-09-02T19:10:04.709123+03:00",
            next_time_to_do="2024-09-02T19:10:04.709123+03:00",
            reward="тест пройден", is_pleasant=False, periodicity=1,
            duration="02:00", is_public=False, is_active=False
        )
        self.data = {
            "name": "Тестовая привычка",
            "place": "В тесте",
            "action": "Протестировать",
            "first_time_to_do": "2024-09-02T19:10:04.709123+03:00",
            "next_time_to_do": "2024-09-02T19:10:04.709123+03:00",
            "reward": "Тест пройден",
            "relation_habit": '',
            "is_pleasant": False,
            "periodicity": 1,
            "duration": "02:00",
            "is_public": False,
            "is_active": True
        }

    def test_habit_create(self):
        url = reverse("tracker:habit_create")
        response = self.client.post(url, self.data)
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )
        self.assertEqual(
            Habit.objects.all().count(), 1
        )

    def test_lesson_update(self):
        url = reverse("tracker:habit_update", args=(self.habit.pk,))
        response = self.client.patch(url, self.data)
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )
        self.assertEqual(
            Habit.objects.get(pk=self.habit.pk).name, "Тестовая привычка для просмотра и изменения"
        )

    def test_habit_delete(self):
        url = reverse("tracker:habit_delete", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )
        self.assertEqual(
            Habit.objects.all().count(), 1
        )

    def test_habit_list(self):
        url = reverse("tracker:habit_list")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )
