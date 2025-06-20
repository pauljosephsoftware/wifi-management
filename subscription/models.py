from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class ServicePlan(models.Model):
    name = models.CharField(max_length=50)
    duration_hours = models.IntegerField()
    bandwidth_limit_mb = models.IntegerField()
    device_limit = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class SubscriberProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(ServicePlan, on_delete=models.SET_NULL, null=True)
    plan_activated = models.DateTimeField(null=True, blank=True)
    plan_expires = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    mac_address = models.CharField(max_length=17, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    def activate_plan(self, plan):
        self.plan = plan
        self.plan_activated = timezone.now()
        self.plan_expires = timezone.now() + timedelta(hours=plan.duration_hours)
        self.save()

class Device(models.Model):
    subscriber = models.ForeignKey(SubscriberProfile, on_delete=models.CASCADE)
    mac_address = models.CharField(max_length=17)
    device_name = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.device_name or self.mac_address}"

class UsageRecord(models.Model):
    subscriber = models.ForeignKey(SubscriberProfile, on_delete=models.CASCADE)
    session_start = models.DateTimeField()
    session_end = models.DateTimeField(null=True, blank=True)
    data_used_mb = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Usage for {self.subscriber.user.username} on {self.session_start}"
    
# model for mpesa payment for the subscription plan chosen
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(ServicePlan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

