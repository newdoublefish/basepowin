# Generated by Django 2.0.8 on 2020-04-09 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MF_MO',
            fields=[
                ('MO_NO', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='单号')),
                ('SO_NO', models.CharField(blank=True, max_length=20, null=True, verbose_name='制定单号')),
            ],
            options={
                'verbose_name': '制定单',
                'verbose_name_plural': '制定单',
                'db_table': 'MF_MO',
            },
        ),
    ]
