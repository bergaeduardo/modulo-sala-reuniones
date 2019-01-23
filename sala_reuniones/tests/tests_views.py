# -*- encoding:utf-8 -*-
# -*- coding:utf-8 -*-


from datetime import datetime, date

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.urls import resolve
from django.contrib.auth.models import User

from sala_reuniones.views import HomeView, ListarReservasViews
from sala_reuniones.models import Insumo, HorarioDisponibilidad, SalaReuniones, Reserva
from sala_reuniones.forms import ReservaForm


class HomeViewTest(TestCase):

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        return self.assertEqual(200, response.status_code)

    def test_home_view_with_class(self):
        view = resolve('/')
        return self.assertEqual(view.func.view_class, HomeView)


class RedirectViewTest(TestCase):
    def setUp(self):
        self.form_data = {'username': 'Frank', 'email': 'f12@eer.er', 'password1': 'qwerty12', 'password2': 'qwerty12'}

    def test_no_users_yet(self):
        self.assertQuerysetEqual([], User.objects.all())

    def test_register_redirection_successful(self):
        response = self.client.post(reverse('registrarse'), self.form_data)
        self.assertEqual(302, response.status_code)

    def test_register_new_user(self):
        response = self.client.post(reverse('registrarse'), self.form_data)
        self.assertTrue(User.objects.all())

    def test_register_new_user_with_name(self):
        response = self.client.post(reverse('registrarse'), self.form_data)
        self.assertEqual('Frank', User.objects.filter(username='Frank').first().username)


class LoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test', is_superuser=True)
        self.user.set_password('1234567a')
        self.user.save()

        self.form_data = {'username': 'test', 'password': '1234567a'}

    def test_login_user_redirect_home(self):
        response = self.client.post(reverse('entrar'), self.form_data)
        self.assertRedirects(response, reverse('home'))


class LogoutViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test', is_superuser=True)
        self.user.set_password('1234567a')
        self.user.save()

        self.client = Client()
        self.client.login(username='test', password='1234567a')

    def test_logout_with_status_code(self):
        response = self.client.get(reverse('salir'))
        self.assertEqual(302, response.status_code)

    def test_logout_redirection_home(self):
        response = self.client.get(reverse('salir'))
        self.assertEqual(response.url, reverse('home'))


class AdicionarReservaViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test', is_superuser=True)
        self.user.set_password('1234567a')
        self.user.save()

        self.insumo = Insumo.objects.create(nombre=u'Pizarrón')
        self.insumo2 = Insumo.objects.create(nombre='Proyector')

        self.horario_disponibilidad1 = HorarioDisponibilidad.objects.create(hora_inicio='10:00', hora_fin='12:00')
        self.horario_disponibilidad2 = HorarioDisponibilidad.objects.create(hora_inicio='13:00', hora_fin='15:00')

        self.sala_reunion = SalaReuniones.objects.create(nombre='Sala 1', ubicacion='Norte', capacidad=10)
        self.sala_reunion.horario_disponibilidad.add(self.horario_disponibilidad1)
        self.sala_reunion.insumos.add(self.insumo)
        self.sala_reunion.save()

        self.client = Client()
        self.client.login(username='test', password='1234567a')

    def test_add_reservation(self):
        form_data = {'fecha': '2019-01-29',
                     'hora_inicio': '10:00',
                     'hora_final': '12:00',
                     'capacidad': 10,
                     'sala_reuniones': self.sala_reunion.pk,
                     'user': self.user.pk
                     }

        form = ReservaForm(form_data, pk=self.sala_reunion.pk)
        self.assertTrue(form.is_valid())

    def test_add_reservation_check_reservation(self):
        form_data = {'fecha': '2019-01-29',
                     'hora_inicio': '10:00',
                     'hora_final': '12:00',
                     'capacidad': 10,
                     'sala_reuniones': self.sala_reunion.pk,
                     'user': self.user.pk
                     }

        form = ReservaForm(form_data, pk=self.sala_reunion.pk)
        form.save()
        self.assertTrue(Reserva.objects.all())

    def test_check_errors_add_reservation_date_past(self):
        form_data = {'fecha': '2019-01-20',
                     'hora_inicio': '10:00',
                     'hora_final': '12:00',
                     'capacidad': 10,
                     'sala_reuniones': self.sala_reunion.pk,
                     'user': self.user.pk
                     }

        form = ReservaForm(form_data, pk=self.sala_reunion.pk)
        self.assertEqual(form.errors['fecha'][0], u'Este campo no admite fechas en el pasado.')

    def test_list_reservations(self):
        response = self.client.get(reverse('sala_reuniones:listar_reservas'))
        self.assertEqual(200, response.status_code)

    def test_list_reservations_check_view(self):
        view = resolve('/sala_reuniones/listar/reservas/')
        self.assertEqual(view.func.view_class, ListarReservasViews)


class EditarReservaViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test', is_superuser=True)
        self.user.set_password('1234567a')
        self.user.save()

        self.insumo = Insumo.objects.create(nombre=u'Pizarrón')
        self.insumo2 = Insumo.objects.create(nombre='Proyector')

        self.horario_disponibilidad1 = HorarioDisponibilidad.objects.create(hora_inicio='10:00', hora_fin='12:00')
        self.horario_disponibilidad2 = HorarioDisponibilidad.objects.create(hora_inicio='13:00', hora_fin='15:00')

        self.sala_reunion = SalaReuniones.objects.create(nombre='Sala 1', ubicacion='Norte', capacidad=10)
        self.sala_reunion.horario_disponibilidad.add(self.horario_disponibilidad1)
        self.sala_reunion.insumos.add(self.insumo)
        self.sala_reunion.save()

        self.reserva = Reserva.objects.create(fecha='2019-01-20', hora_inicio='10:00',
                                              hora_final='12:00', capacidad=10, sala_reuniones=self.sala_reunion,
                                              user=self.user)

        self.form_data = {'fecha': '2019-01-28',
                          'hora_inicio': '10:00',
                          'hora_final': '12:00',
                          'capacidad': 50,
                          'sala_reuniones': self.sala_reunion.pk,
                          'user': self.user.pk
                          }

        self.client = Client()
        self.client.login(username='test', password='1234567a')

    def test_edit_with_url(self):
        response = self.client.post(reverse('sala_reuniones:editar_reserva',
                                            kwargs={'pk': self.reserva.pk}), self.form_data)

        self.assertEqual(302, response.status_code)

    def test_edit_field_capacidad(self):
        response = self.client.post(reverse('sala_reuniones:editar_reserva',
                                            kwargs={'pk': self.reserva.pk}), self.form_data)
        reserva = Reserva.objects.get(pk=self.reserva.pk).capacidad
        self.assertEqual(50, reserva)


class EliminarReservasViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test', is_superuser=True)
        self.user.set_password('1234567a')
        self.user.save()

        self.insumo = Insumo.objects.create(nombre=u'Pizarrón')
        self.insumo2 = Insumo.objects.create(nombre='Proyector')

        self.horario_disponibilidad1 = HorarioDisponibilidad.objects.create(hora_inicio='10:00', hora_fin='12:00')
        self.horario_disponibilidad2 = HorarioDisponibilidad.objects.create(hora_inicio='13:00', hora_fin='15:00')

        self.sala_reunion = SalaReuniones.objects.create(nombre='Sala 1', ubicacion='Norte', capacidad=10)
        self.sala_reunion.horario_disponibilidad.add(self.horario_disponibilidad1)
        self.sala_reunion.insumos.add(self.insumo)
        self.sala_reunion.save()

        self.reserva = Reserva.objects.create(fecha='2019-01-20', hora_inicio='10:00',
                                              hora_final='12:00', capacidad=10, sala_reuniones=self.sala_reunion,
                                              user=self.user)

        self.client = Client()
        self.client.login(username='test', password='1234567a')

    def test_delete_status_code(self):
        response = self.client.post(reverse('sala_reuniones:eliminar_reserva', kwargs={'pk': self.reserva.pk}))
        self.assertEqual(response.status_code, 302)

    def test_delete_redirection(self):
        response = self.client.post(reverse('sala_reuniones:eliminar_reserva', kwargs={'pk': self.reserva.pk}))
        self.assertRedirects(response, reverse('sala_reuniones:listar_reservas'))

    def test_delete_reserva_query(self):
        response = self.client.post(reverse('sala_reuniones:eliminar_reserva', kwargs={'pk': self.reserva.pk}))
        self.assertQuerysetEqual([], Reserva.objects.all())
