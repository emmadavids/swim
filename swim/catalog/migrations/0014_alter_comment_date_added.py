# Generated by Django 4.0.3 on 2022-06-24 20:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_alter_comment_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 24, 20, 44, 13, 453979, tzinfo=utc), max_length=64),
        ),
    ]
