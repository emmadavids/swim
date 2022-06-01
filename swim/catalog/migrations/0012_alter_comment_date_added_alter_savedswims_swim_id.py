# Generated by Django 4.0.3 on 2022-06-01 10:22

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_alter_comment_date_added_alter_photo_swim_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 1, 10, 22, 43, 61069, tzinfo=utc), max_length=64),
        ),
        migrations.AlterField(
            model_name='savedswims',
            name='swim_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='catalog.swimspot'),
        ),
    ]
