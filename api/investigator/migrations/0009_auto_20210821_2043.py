# Generated by Django 3.2.6 on 2021-08-21 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investigator', '0008_codes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codes',
            name='created',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='codes',
            name='used',
            field=models.DateTimeField(null=True),
        ),
    ]
