"""SIGRES URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from sala_reuniones.views import RegisterView, HomeView
app_name = "sala_reuniones"

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^registrarse/$', RegisterView.as_view(), name='registrarse'),
    url(r'login/$', LoginView.as_view(template_name='sala_reuniones/entrar.html'), name='entrar'),
    url(r'^salir/$', LogoutView.as_view(), name='salir'),
    url(r'^sala_reuniones/', include(('sala_reuniones.urls'), namespace='sala_reuniones')),
    url(r'^$', HomeView.as_view(), name='home'),
]
