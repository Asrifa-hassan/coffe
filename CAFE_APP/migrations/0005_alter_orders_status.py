# Generated by Django 5.1.4 on 2025-04-04 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CAFE_APP', '0004_alter_orders_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.CharField(choices=[(1, 'Ordered'), (2, 'Pending'), (3, 'Delivered'), (4, 'Cancelled')], default=1, max_length=200),
        ),
    ]
