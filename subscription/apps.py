from django.apps import AppConfig



class SubscriptionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subscription'

# apps.py
def ready(self):
    import subscription.signals

from mpesa import*  # or wherever your module lives
