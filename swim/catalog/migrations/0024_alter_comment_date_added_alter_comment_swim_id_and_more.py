# Generated by Django 4.0.3 on 2022-04-21 19:25

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0023_alter_comment_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 21, 19, 25, 58, 509307, tzinfo=utc), max_length=64),
        ),
        migrations.AlterField(
            model_name='comment',
            name='swim_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='catalog.swimspot'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='swim_id',
            field=models.CharField(default='swim_id', max_length=100),
        ),
    ]
