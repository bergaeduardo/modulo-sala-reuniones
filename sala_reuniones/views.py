# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from distutils import errors
from distutils.log import ERROR

from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, View, TemplateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User

from .models import SalaReuniones, Reserva
from .forms import UserRegisterForm, ReservaForm

from braces.views import LoginRequiredMixin, FormValidMessageMixin
from datetime import datetime, timedelta


# Create your views here.


class HomeView(ListView):
    model = SalaReuniones
    template_name = 'sala_reuniones/home.html'
    context_object_name = 'salas_reuniones'

    def get_context_data(self, *args, **kwargs):
        context_data = super(HomeView, self).get_context_data(*args, **kwargs)
        reserva=Reserva.objects.filter(fecha=datetime.now().date()).order_by('fecha')        
        context_data['reservas'] = reserva
        print(reserva)
        
        return context_data


class RegisterView(View):
    template_name = 'sala_reuniones/register.html'

    def get(self, request, *args, **kwargs):
        form = UserRegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            messages.success(request, 'Cuenta creada para %s !!!' % username)
            form.save()
            return redirect('home')
        return render(request, self.template_name, {'form': form})


class AdicionarReservaView(LoginRequiredMixin, CreateView):
    model = Reserva
    form_class = ReservaForm
    success_url = reverse_lazy('sala_reuniones:calendario_reservas')

    def form_valid(self, form):
        formulario = form.save(commit=False)
        formulario.user = self.request.user

        # if formulario.confirmada:
        #     formulario.estado = Reserva.CONFIRMADA
        # else:
        #     formulario.estado = Reserva.RESERVADA
        formulario.estado = Reserva.CONFIRMADA

        formulario.save()

        return super(AdicionarReservaView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context_data = super(AdicionarReservaView, self).get_context_data(*args, **kwargs)
        sala_reunion = SalaReuniones.objects.get(pk=self.kwargs['pk'])
        hoy = datetime.date(datetime.now())
        Dia_reserva= hoy


        context_data['sala_reunion'] = sala_reunion
        context_data['horarios'] = sala_reunion.horario_disponibilidad.all()
        context_data['aux'] = hoy
        context_data['aux2'] = Dia_reserva
        # error = ReservaForm.hora_final.error_messages
        # print(error)
        

        return context_data

    def get_form_kwargs(self):
        kwargs = super(AdicionarReservaView, self).get_form_kwargs()
        kwargs['pk'] = self.kwargs['pk']
        return kwargs

    


class ListarReservasViews(ListView):
    model = Reserva
    context_object_name = 'reservas'


class ReservasFullcalendario(TemplateView):
    template_name = 'sala_reuniones/fullcalendar.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super(ReservasFullcalendario, self).get_context_data(*args, **kwargs)
        context_data['reservas'] = Reserva.objects.all()
        # print(context_data['reservas'])
        return context_data


class EditarReservaView(LoginRequiredMixin, FormValidMessageMixin, UpdateView):
    model = Reserva
    form_class = ReservaForm
    form_valid_message = 'Se ha editado la reserva satisfactoriamente.'
    success_url = reverse_lazy('sala_reuniones:calendario_reservas')

    def get_context_data(self, *args, **kwargs):
        reserva = Reserva.objects.get(pk=self.kwargs['pk'])
        hoy = datetime.date(datetime.now())
        Dia_reserva = reserva.fecha


        context_data = super(EditarReservaView, self).get_context_data(*args, **kwargs)
        context_data['sala_reunion'] = reserva.sala_reuniones
        context_data['horarios'] = reserva.sala_reuniones.horario_disponibilidad.all()
        context_data['editar'] = True
        context_data['pk'] = self.object.pk
        context_data['aux'] = hoy
        context_data['aux2'] = Dia_reserva

        

        return context_data

    # @property
    # def is_past_due(self):
    #     aux = datetime.date.today()
    #     return aux


class EliminarReservasView(LoginRequiredMixin, DeleteView):
    model = Reserva
    success_url = reverse_lazy('sala_reuniones:listar_reservas')
