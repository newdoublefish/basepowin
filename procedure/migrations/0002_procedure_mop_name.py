# Generated by Django 2.0.8 on 2020-03-24 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procedure', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='procedure',
            name='mop_name',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='制订单流程'),
        ),
    ]
