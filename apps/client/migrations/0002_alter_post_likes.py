# Generated by Django 4.2.1 on 2023-05-17 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
