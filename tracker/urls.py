from django.urls import path

from tracker.apps import TrackerConfig
from tracker.views import HabitCreateAPIView, HabitRetrieveAPIView, \
    HabitDestroyAPIView, HabitUpdateAPIView, PublicHabitListAPIView, \
    HabitListAPIView

app_name = TrackerConfig.name


urlpatterns = [
    path('habit_create/', HabitCreateAPIView.as_view(), name='habit_create'),
    path('habit_detail/<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit_detail'),
    path('habit_list/', HabitListAPIView.as_view(), name='habit_list'),
    path('public_habit_list/', PublicHabitListAPIView.as_view(), name='public_habit_list'),
    path('habit_update/<int:pk>/', HabitUpdateAPIView.as_view(), name='habit_update'),
    path('habit_delete/<int:pk>/', HabitDestroyAPIView.as_view(), name='habit_delete'),
]
