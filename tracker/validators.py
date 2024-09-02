from datetime import timedelta
from rest_framework import serializers


def validate_duration(duration):
    try:
        duration = duration.split(':')
        if len(duration) != 2:
            raise TypeError("Длительность должна быть в формате MM:SS, пример - 01:33")
        minute = duration[0]
        second = duration[1]
        duration = timedelta(minutes=int(minute), seconds=int(second))
    except TypeError as ex:
        raise serializers.ValidationError(ex)
    if duration > timedelta(minutes=2):
        raise serializers.ValidationError("Длительность должна быть не более 2 минут")
