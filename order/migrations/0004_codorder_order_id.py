# Generated by Django 5.0.2 on 2024-02-29 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_codpurchaseproduct_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='codorder',
            name='order_id',
            field=models.CharField(editable=False, max_length=100, null=True, unique=True),
        ),
    ]
