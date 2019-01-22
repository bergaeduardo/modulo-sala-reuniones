# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import HorarioDisponibilidad, SalaReuniones, Insumo, Reserva

# Register your models here.
admin.site.register(SalaReuniones)
admin.site.register(Insumo)
admin.site.register(HorarioDisponibilidad)
admin.site.register(Reserva)