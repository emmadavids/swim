# Generated by Django 4.0.3 on 2022-05-15 16:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_alter_comment_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 15, 16, 41, 52, 105108, tzinfo=utc), max_length=64),
        ),
    ]
