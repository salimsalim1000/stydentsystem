# Generated by Django 3.0.7 on 2020-08-09 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_auto_20200803_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaveraportstudent',
            name='leave_status',
            field=models.IntegerField(default=0),
        ),
    ]