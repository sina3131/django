# Generated by Django 4.2.2 on 2023-07-12 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cybersec', '0002_device'),
    ]

    operations = [
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(max_length=100)),
            ],
        ),
    ]