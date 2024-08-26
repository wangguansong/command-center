# Generated by Django 5.1 on 2024-08-25 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0002_alter_posting_posting_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postingcompany',
            name='company',
        ),
        migrations.RemoveField(
            model_name='position',
            name='company',
        ),
        migrations.RemoveField(
            model_name='posting',
            name='position',
        ),
        migrations.RemoveField(
            model_name='posting',
            name='posting_company',
        ),
        migrations.DeleteModel(
            name='Company',
        ),
        migrations.DeleteModel(
            name='Position',
        ),
        migrations.DeleteModel(
            name='Posting',
        ),
        migrations.DeleteModel(
            name='PostingCompany',
        ),
    ]
