from rest_framework import serializers
from tracker.models import Habit
from tracker.validators import validate_duration


class HabitSerializer(serializers.ModelSerializer):
    duration = serializers.CharField(validators=[validate_duration], required=False)
    periodicity = serializers.IntegerField(min_value=1, max_value=7, required=False)

    def validate(self, data):
        if data.get('is_pleasant') and (data.get('reward') or data.get('relation_habit')):
            raise serializers.ValidationError(
                'У приятной привычки не может быть '
                'вознаграждения или связанной привычки')
        if not data.get('is_pleasant'):
            if not (data.get('reward') or data.get('relation_habit')):
                raise serializers.ValidationError(
                    'У полезной привычки должно быть '
                    'вознаграждение или связанная привычка')
            if data.get('reward') and data.get('relation_habit'):
                raise serializers.ValidationError(
                    'У полезной привычки не может быть одновременно и'
                    'вознаграждение и связанная привычка')
            if data.get('relation_habit') and not data.get('relation_habit').is_pleasant:
                raise serializers.ValidationError(
                    'В связанные привычки могут попадать только '
                    ' приятные привычки')
        return data

    class Meta:
        model = Habit
        fields = ('name', 'place', 'action', 'first_time_to_do',
                  'reward', 'relation_habit', 'is_pleasant',
                  'periodicity', 'duration', 'is_public', 'is_active')
        extra_kwargs = {'owner': {'required': False}}
