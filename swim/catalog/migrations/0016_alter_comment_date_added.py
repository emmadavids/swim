# Generated by Django 4.0.3 on 2022-04-20 13:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0015_alter_comment_date_added_alter_swimspot_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 20, 13, 46, 51, 987634, tzinfo=utc), max_length=64),
        ),
    ]
