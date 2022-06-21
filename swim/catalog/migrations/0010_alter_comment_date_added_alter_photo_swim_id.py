# Generated by Django 4.0.3 on 2022-05-22 19:02

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_alter_comment_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 22, 19, 2, 59, 189511, tzinfo=utc), max_length=64),
        ),
        migrations.AlterField(
            model_name='photo',
            name='swim_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='catalog.swimspot'),
        ),
    ]