# Generated by Django 2.1.5 on 2020-04-11 15:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procedure', '0014_auto_20200411_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 4, 11, 23, 59, 44, 417331), null=True, verbose_name='创建时间'),
        ),
    ]
