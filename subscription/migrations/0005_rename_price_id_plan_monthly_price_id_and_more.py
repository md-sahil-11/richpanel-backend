# Generated by Django 4.0.4 on 2022-10-02 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0004_subscriptionhistory_delete_subscription_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plan',
            old_name='price_id',
            new_name='monthly_price_id',
        ),
        migrations.AddField(
            model_name='plan',
            name='yearly_price_id',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
