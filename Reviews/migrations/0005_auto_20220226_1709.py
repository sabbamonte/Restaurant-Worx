# Generated by Django 3.1.5 on 2022-02-26 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reviews', '0004_auto_20220226_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='location',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='info',
            name='position',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
