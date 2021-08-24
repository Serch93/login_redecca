# Generated by Django 3.2.6 on 2021-08-21 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investigator', '0009_auto_20210821_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connectionslogs',
            name='action',
            field=models.CharField(choices=[('CI', 'Creación de Investigador'), ('LI', 'Log-In'), ('LO', 'Log-Out'), ('SRC', 'Solicitud de restablecimiento de contraseña'), ('VRC', 'Validar código de recuperación de contraseña'), ('OIU', 'Obtener información de usuario')], default='LI', max_length=250),
        ),
    ]