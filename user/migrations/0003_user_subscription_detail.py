# Generated by Django 4.0.4 on 2022-10-01 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='subscription_detail',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
