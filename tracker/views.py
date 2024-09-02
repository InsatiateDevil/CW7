from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from tracker.models import Habit
from tracker.paginators import CustomPaginator
from tracker.permissions import IsOwner, IsPublic
from tracker.serializers import HabitSerializer
from tracker.tasks import send_notification


# Create your views here.
class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        next_time_to_do = serializer.validated_data['first_time_to_do']
        habit = serializer.save(owner=self.request.user, next_time_to_do=next_time_to_do)
        if self.request.user.telegram_chat_id:
            chat_id = self.request.user.telegram_chat_id
            habit_id = habit.id
            send_notification.apply_async((habit_id, chat_id,),
                                          eta=habit.next_time_to_do)
        else:
            habit.is_active = False
            habit.save()


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsAuthenticated, IsPublic | IsOwner)


class HabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    pagination_class = CustomPaginator

    def get_queryset(self):
        return Habit.objects.filter(owner=self.request.user)


class PublicHabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    pagination_class = CustomPaginator

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)


class HabitUpdateAPIView(generics.UpdateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)


class HabitDestroyAPIView(generics.DestroyAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)
