# Generated by Django 4.0.3 on 2022-05-12 19:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_profilepic_remove_userprofile_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 12, 19, 45, 46, 51301, tzinfo=utc), max_length=64),
        ),
    ]
