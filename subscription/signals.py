# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import SubscriberProfile
from mpesa.models import MpesaPayment
from .models import*

User = get_user_model()
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        SubscriberProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.subscriberprofile.save()

@receiver(post_save, sender=MpesaPayment)
def handle_mpesa_callback(sender, instance, created, **kwargs):
    if not created:
        return
    if instance.ResultCode == '0':  # Payment successful
        # Extract plan from account_reference, e.g. "Plan-3"
        account_ref = instance.AccountReference or instance.account_reference
        plan_id = int(account_ref.split('-')[1])
        plan = ServicePlan.objects.get(pk=plan_id)

        # Lookup user (link via phone or store association earlier)
        profile = SubscriberProfile.objects.filter(phone_number=instance.MSISDN).first()
        if profile:
            # Create or update subscription
            ServicePlan.objects.create(
                subscriber=profile,
                plan=plan,
                expires=timezone.now() + timedelta(hours=plan.duration_hours),
                checkout_id=instance.CheckoutRequestID,
            )