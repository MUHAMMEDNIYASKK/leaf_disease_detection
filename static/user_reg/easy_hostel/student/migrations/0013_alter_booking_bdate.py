# Generated by Django 3.2.8 on 2021-12-03 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0012_alter_booking_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='bdate',
            field=models.CharField(max_length=20),
        ),
    ]