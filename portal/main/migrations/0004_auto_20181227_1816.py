# Generated by Django 2.1.4 on 2018-12-27 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20181226_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='insured_value',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='customer',
            name='prev_claim_revoked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customer',
            name='prev_insurance_amt',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='customer',
            name='prev_insurance_no',
            field=models.IntegerField(default=0),
        ),
    ]