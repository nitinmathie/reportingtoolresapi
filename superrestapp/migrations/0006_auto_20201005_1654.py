# Generated by Django 3.1.1 on 2020-10-05 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superrestapp', '0005_auto_20201005_1609'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_created_by',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_updated_by',
        ),
    ]
