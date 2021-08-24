from django.db import models
from django.utils import timezone


class Server(models.Model):
    name = models.CharField(
        verbose_name='Nombre de servidor', max_length=100, null=False, blank=False)
    memory = models.IntegerField(verbose_name='Memoria', null=False, blank=False)
    volume = models.IntegerField(verbose_name='Volumen', null=False, blank=False)
    cpu = models.IntegerField(verbose_name='CPU', null=False, blank=False)
    price = models.FloatField(verbose_name='Precio', null=False, blank=False)
    so = models.CharField(
        verbose_name='Sistema Operativo', max_length=100, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(null=True)
    updated = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.pk}: {self.name} -> {self.so}'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Servidor'
        verbose_name_plural = 'Listado de servidores'
