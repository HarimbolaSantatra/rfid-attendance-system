# Generated by Django 3.1.3 on 2022-09-07 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_auto_20220907_1504'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendancerecord',
            old_name='card_id',
            new_name='user',
        ),
    ]
