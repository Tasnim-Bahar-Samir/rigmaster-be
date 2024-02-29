# Generated by Django 5.0.2 on 2024-02-29 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codorder',
            name='payment_status',
            field=models.CharField(choices=[('UNPAID', 'Unpaid'), ('PAID', 'Paid'), ('PERCIAL_PAID', 'Partial Paid')], default='UNPAID', max_length=20),
        ),
    ]
