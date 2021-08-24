# Generated by Django 3.2.6 on 2021-08-21 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('investigator', '0003_auto_20210821_1532'),
    ]

    operations = [
        migrations.CreateModel(
            name='Investigator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('created', models.DateTimeField()),
                ('last_login', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Investigador',
                'verbose_name_plural': 'Listado de Investigadores',
                'ordering': ['pk'],
            },
        ),
        migrations.RemoveField(
            model_name='connectionslogs',
            name='email',
        ),
        migrations.RemoveField(
            model_name='connectionslogs',
            name='session_state',
        ),
        migrations.AlterField(
            model_name='connectionslogs',
            name='action',
            field=models.CharField(choices=[('CI', 'Creación de Investigador'), ('LI', 'Log-In'), ('LO', 'Log-Out'), ('SRC', 'Solicitud de restablecimiento de contraseña'), ('ERC', 'Enviar código de recuperación de Contraseña'), ('VRC', 'Validar código de recuperación de contraseña'), ('RC', 'Restablecer contraseña'), ('OIU', 'Obtener información de usuario')], default='LI', max_length=250),
        ),
        migrations.AddField(
            model_name='connectionslogs',
            name='investigador',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='investigator.investigator'),
        ),
    ]