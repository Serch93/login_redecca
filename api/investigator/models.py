from django.db import models
from django.utils import timezone


class Investigator(models.Model):
    email = models.EmailField(null=False, blank=False)
    created = models.DateTimeField()
    last_login = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    id_keyclock = models.CharField(null=True, max_length=100)
    curp = models.CharField(null=True, max_length=100)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.last_login = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.pk}: {self.email} -> {self.is_active}'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Investigador'
        verbose_name_plural = 'Listado de Investigadores'


class ConnectionsLogs(models.Model):
    CHOICES_OPTIONS_ACTIONS = [
        ('CI', 'Creación de Investigador'),
        ('LI', 'Log-In'),
        ('LO', 'Log-Out'),
        ('SRC', 'Solicitud de restablecimiento de contraseña'),
        ('VRC', 'Validar código de recuperación de contraseña'),
        ('OIU', 'Obtener información de usuario'),
    ]

    investigador = models.ForeignKey(
        Investigator, on_delete=models.CASCADE, related_name='logs', null=True)
    status_server = models.CharField(null=True, max_length=50, blank=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    action = models.CharField(
        null=False,
        blank=False,
        max_length=250,
        choices=CHOICES_OPTIONS_ACTIONS,
        default='LI'
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pk}: {self.investigador.email} -> {self.action} ({self.status_server})"

    class Meta:
        ordering = ['pk']
        verbose_name = 'Registro de Conexión'
        verbose_name_plural = 'Logs de Solicitudes de Conexión'


class Codes(models.Model):
    investigator = models.ForeignKey(
        Investigator, on_delete=models.CASCADE, null=True, related_name='codes')
    code = models.CharField(max_length=255, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(null=True)
    used = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pk}: {self.investigator.email} -> {self.code}"

    class Meta:
        ordering = ['pk']
        verbose_name = 'Código de activación'
        verbose_name_plural = 'Listado de códigos'
