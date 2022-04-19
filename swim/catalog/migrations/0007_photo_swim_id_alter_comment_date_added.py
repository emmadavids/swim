# Generated by Django 4.0.3 on 2022-04-15 19:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_alter_comment_date_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='swim_id',
            field=models.CharField(default='0', max_length=100),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 15, 19, 43, 6, 174402, tzinfo=utc), max_length=64),
        ),
    ]
