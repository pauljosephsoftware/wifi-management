# Generated by Django 5.2.3 on 2025-06-19 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriberprofile',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subscriberprofile',
            name='mac_address',
            field=models.CharField(blank=True, max_length=17, null=True),
        ),
    ]
