from django.db import models
from datetime import datetime, timedelta


class User(models.Model):

    STATUS_CHOICE = (
        ('a', 'accepted'),
        ('r', 'refused')
    )
    GENDER_CHOICE = (
        ('m', 'male'),
        ('f', 'female'),
    )
    name = models.CharField(max_length=100)
    card_id = models.CharField(max_length=15)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1,
                              choices=GENDER_CHOICE,
                              null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICE, default='a')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        accepted_card_id = ["33 27 04 03", "0C BD F3 16"]
        if self.card_id in accepted_card_id:
            self.status = 'a'
        else:
            self.status = 'r'

    def __str__(self):
        return self.name


class AttendanceRecordManager(models.Manager):
    # This manager returns all AttendanceRecord which recording dates is less than a day

    def get_today(self):
        yesterday = datetime.now() - timedelta(hours=24)
        return super().get_queryset().filter(date__gte=yesterday)


class AttendanceRecord(models.Model):

    # Usually, a primary key field will automatically be added,
    # but I use this to have more control
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)

    # We made a custom manager, so we have to remake the original manager
    objects = models.Manager()
    # Instantiating the manager
    custom_manager = AttendanceRecordManager()

    def __str__(self):
        return str(self.date)
