# Generated by Django 4.1 on 2022-08-19 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posting',
            name='posting_status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Normal'), (1, 'Closed'), (2, 'Inactive')], default=0),
        ),
    ]
