# -*- encoding:utf-8 -*-
# -*- coding:utf-8 -*-


from datetime import datetime, date

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.urls import resolve
from django.contrib.auth.models import User

from sala_reuniones.views import HomeView
from sala_reuniones.models import Insumo, HorarioDisponibilidad, SalaReuniones


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


# class AdicionarReservaViewTest(TestCase):

#     def setUp(self):
#         self.user = User.objects.create(username='test', is_superuser=True)
#         self.user.set_password('1234567a')
#         self.user.save()

#         self.insumo = Insumo.objects.create(nombre=u'Pizarrón')
#         self.insumo2 = Insumo.objects.create(nombre='Proyector')

#         self.horario_disponibilidad1 = HorarioDisponibilidad.objects.create(hora_inicio='10:00', hora_fin='12:00')
#         self.horario_disponibilidad2 = HorarioDisponibilidad.objects.create(hora_inicio='13:00', hora_fin='15:00')

#         self.sala_reunion = SalaReuniones(nombre='Sala 1', ubicacion='Norte', capacidad=10, horario_disponibilidad=[
#                                           self.horario_disponibilidad1], insumos=[self.insumo])




