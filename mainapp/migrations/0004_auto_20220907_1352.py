# Generated by Django 3.1.3 on 2022-09-07 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_rfiddata_userdata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rfiddata',
            name='username',
        ),
        migrations.AlterField(
            model_name='rfiddata',
            name='card_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainapp.userdata'),
        ),
    ]
