# Generated by Django 3.0.7 on 2020-06-14 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzaApp', '0007_auto_20200611_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signupmodel',
            name='phone',
            field=models.CharField(max_length=10),
        ),
    ]