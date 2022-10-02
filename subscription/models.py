from django.db import models

from user.models import User


class Device(models.Model):
    name = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.name


class Plan(models.Model):
    membership_type = (
        ('monthly', 'monthly'),
        ('yearly', 'yearly')
    )
    price_id = models.CharField(max_length=250, null=True, blank=True)
    plan_name = models.CharField(max_length=50, null=True)
    price = models.FloatField(default=0.0, null=True, blank=True)
    membership = models.CharField(max_length=100, choices=membership_type, null=True, blank=True)
    video_quality = models.CharField(max_length=250, null=True)
    resolution = models.CharField(max_length=250, null=True)
    devices = models.ManyToManyField(Device, related_name='plans')
    screens = models.IntegerField(default=0)

    def __str__(self):
        return self.plan_name


class SubscriptionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True)
    is_cancelled = models.BooleanField(default=False)