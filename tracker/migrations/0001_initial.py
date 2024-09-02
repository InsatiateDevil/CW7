# Generated by Django 4.2.13 on 2024-09-01 12:46

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='название привычки')),
                ('place', models.CharField(max_length=100, verbose_name='место выполнения действия')),
                ('action', models.CharField(blank=True, max_length=255, null=True, verbose_name='действие')),
                ('first_time_to_do', models.DateTimeField(verbose_name='дата первого выполнения привычки')),
                ('next_time_to_do', models.DateTimeField(blank=True, verbose_name='дата следующего выполнения привычки')),
                ('reward', models.CharField(blank=True, max_length=100, null=True, verbose_name='вознаграждение за выполнение привычки')),
                ('is_pleasant', models.BooleanField(blank=True, default=False, null=True, verbose_name='приятность привычки')),
                ('periodicity', models.PositiveSmallIntegerField(blank=True, default=1, verbose_name='периодичность в днях')),
                ('duration', models.CharField(blank=True, default=datetime.timedelta(seconds=120), max_length=50, verbose_name='время требующееся на выполнение действия')),
                ('is_public', models.BooleanField(blank=True, default=False, verbose_name='доступность другим пользователям')),
                ('is_active', models.BooleanField(blank=True, default=True, verbose_name='активность привычки(влияет на отправку уведомлений пользователю)')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='создатель привычки')),
                ('relation_habit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tracker.habit', verbose_name='связующая привычка')),
            ],
            options={
                'verbose_name': 'привычка',
                'verbose_name_plural': 'привычки',
            },
        ),
    ]
