# Generated by Django 3.2.6 on 2021-08-21 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investigator', '0004_auto_20210821_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='investigator',
            name='id_keyclock',
            field=models.IntegerField(null=True),
        ),
    ]