# -*- encoding:utf-8 -*-
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings


# Create your models here.


class Insumo(models.Model):
    nombre = models.CharField(max_length=30)

    class Meta:
        ordering = ['nombre']

    def __unicode__(self):
        return unicode(self.nombre)

    def __str__(self):
        return self.nombre


class HorarioDisponibilidad(models.Model):
    hora_inicio = models.TimeField(verbose_name='Hora de inicio')
    hora_fin = models.TimeField(verbose_name='Hora de terminar')

    class Meta:
        ordering = ['hora_inicio']
        verbose_name_plural = 'Horario disponibilidades'

    def __unicode__(self):
        return unicode(str(self.hora_inicio) + ' - ' + str(self.hora_fin))

    def __str__(self):
        return str(self.hora_inicio) + ' - ' + str(self.hora_fin)


class SalaReuniones(models.Model):
    nombre = models.CharField(max_length=50)
    ubicacion = models.CharField(max_length=100, verbose_name=u'Ubicación')
    capacidad = models.IntegerField()
    horario_disponibilidad = models.ManyToManyField(HorarioDisponibilidad)
    insumos = models.ManyToManyField(Insumo, default=['Proyector', u'Pizarrón'], blank=True)

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = 'Sala de reuniones'

    def __unicode__(self):
        return unicode(self.nombre)

    def __str__(self):
        return self.nombre


class Reserva(models.Model):
    NO_DISPONIBLE = 'nd'
    DISPONIBLE = 'd'
    RESERVADA = 'r'
    CONFIRMADA = 'c'

    ESTADO_CHOICES = (
        (NO_DISPONIBLE, 'No disponible'),
        (DISPONIBLE, 'Disponible'),
        (RESERVADA, 'Reservada'),
        (CONFIRMADA, 'Confirmada')
    )

    fecha = models.DateField()
    hora_inicio = models.TimeField(verbose_name='Hora inicial')
    hora_final = models.TimeField(verbose_name='Hora final')
    capacidad = models.IntegerField(verbose_name='Capacidad de personas', default=10)
    sala_reuniones = models.ForeignKey(SalaReuniones, on_delete=models.DO_NOTHING,default=1)
    confirmada = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=DISPONIBLE)

    class Meta:
        ordering = ['fecha', 'sala_reuniones']

    def __str__(self):
        return (str(self.fecha) + ' ' + self.sala_reuniones.nombre + ' ' + str(self.hora_inicio.strftime('%H:%M')) + ' ' + str(self.hora_final.strftime('%H:%M')))
        # .strftime('%d-%b-%Y')
