# Generated by Django 4.0.4 on 2022-10-02 06:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djstripe', '0011_alter_invoiceitem_tax_rates_and_more'),
        ('user', '0003_user_subscription_detail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='subscription_detail',
        ),
        migrations.AddField(
            model_name='user',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='djstripe.customer'),
        ),
        migrations.AddField(
            model_name='user',
            name='subscription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='djstripe.subscription'),
        ),
    ]
