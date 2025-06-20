from django.contrib import admin
from .models import*
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
# Register your models here.
admin.site.register(ServicePlan),
admin.site.register(Device),
admin.site.register(UsageRecord),
admin.site.register(SubscriberProfile),



class ServicePlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_hours', 'bandwidth_limit_mb', 'price')

class UsageRecordAdmin(admin.ModelAdmin):
    list_filter = (
        ('session_start', DateRangeFilter),
        ('session_end', DateTimeRangeFilter),
    )