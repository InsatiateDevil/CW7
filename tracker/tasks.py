from datetime import timedelta

import requests
from celery import shared_task

from config.settings import TELEGRAM_BOT_TOKEN
from tracker.models import Habit


@shared_task
def send_notification(habit_id, chat_id):
    habit = Habit.objects.get(id=habit_id)
    if habit.relation_habit:
        message = (f"Уведомляем вас о необходимости выполнить {habit.action},"
                   f" а затем {habit.relation_habit.action}")
    else:
        message = (f"Уведомляем вас о необходимости выполнить {habit.action},"
                   f" а затем получить вознаграждение в виде - {habit.reward}")
    params = {
        "text": message,
        "chat_id": chat_id,
    }
    requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", params=params)
    habit.next_time_to_do += timedelta(days=habit.periodicity)
    send_notification.apply_async((habit_id, chat_id,), eta=habit.next_time_to_do)
