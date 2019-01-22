# -*- encoding:utf-8 -*-
# -*- coding:utf-8 -*-

from datetime import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Reserva, SalaReuniones
from .widgets import DatePicker, TimePicker


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ReservaForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Reserva
        fields = ['fecha', 'hora_inicio', 'hora_final', 'capacidad', 'sala_reuniones', 'confirmada', 'user']
        widgets = {
            'fecha': DatePicker,
            'hora_inicio': TimePicker,
            'hora_final': TimePicker
        }

    def __init__(self, *args, **kwargs):

        if 'pk' in kwargs:
            pk_sala = kwargs.pop('pk')

        super(ReservaForm, self).__init__(*args, **kwargs)
        if not self.instance.id:
            sala_reunion = SalaReuniones.objects.get(pk=pk_sala)
            self.fields['user'].required = False
            self.fields['sala_reuniones'].initial = sala_reunion

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']

        if fecha < datetime.now().date():
            raise forms.ValidationError('Este campo no admite fechas en el pasado.')

        return fecha

    def clean_hora_final(self):
        hora_final = self.cleaned_data['hora_final']

        try:
            hora_inicio = self.cleaned_data['hora_inicio']
        except KeyError:
            hora_inicio = ''

        if hora_inicio:
            if hora_final < hora_inicio:
                raise forms.ValidationError('La hora final no puede ser menor que la hora inicial.')

        return hora_final

    def clean_sala_reuniones(self):
        sala_reunion = self.cleaned_data['sala_reuniones']

        try:
            hora_inicio = self.cleaned_data['hora_inicio']
            hora_final = self.cleaned_data['hora_final']
        except KeyError:
            return sala_reunion

        for horario in sala_reunion.horario_disponibilidad.all():
            if hora_inicio < horario.hora_inicio or hora_inicio > horario.hora_fin:
                self.add_error('hora_inicio', 'No hay disponibilidad a esta hora.')
            if hora_final < horario.hora_inicio or hora_final > horario.hora_fin:
                self.add_error('hora_final', 'No hay disponibilidad en este horario.')

        return sala_reunion

    def clean(self):

        try:
            fecha = self.cleaned_data['fecha']
            hora_inicio = self.cleaned_data['hora_inicio']
            hora_final = self.cleaned_data['hora_final']

        except KeyError:
            return self.cleaned_data

        reserva = Reserva.objects.filter(fecha=fecha, hora_inicio=hora_inicio, hora_final=hora_final)

        if reserva:
            raise forms.ValidationError('Ya existe una reserva en esa fecha y rango de horarios.')

        return self.cleaned_data
