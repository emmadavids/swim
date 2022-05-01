# Generated by Django 4.0.3 on 2022-04-25 19:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0024_alter_comment_date_added_alter_comment_swim_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='swimspot',
            name='distance_suitable',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 25, 19, 22, 58, 286254, tzinfo=utc), max_length=64),
        ),
    ]
