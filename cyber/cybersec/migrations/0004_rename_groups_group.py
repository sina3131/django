# Generated by Django 4.2.2 on 2023-07-12 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cybersec', '0003_groups'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Groups',
            new_name='Group',
        ),
    ]
