from django.conf.urls import url

from .views import (AdicionarReservaView,
                    ListarReservasViews,
                    ReservasFullcalendario,
                    EditarReservaView,
                    EliminarEventosView)


urlpatterns = [

    url(r'^adicionar/reserva/(?P<pk>\d+)/$', AdicionarReservaView.as_view(), name='adicionar_reserva'),
    url(r'^listar/reservas/$', ListarReservasViews.as_view(), name='listar_reservas'),
    url(r'^listar/reservas/calendario/$', ReservasFullcalendario.as_view(), name='calendario_reservas'),
    url(r'^editar/reserva/(?P<pk>\d+)/$', EditarReservaView.as_view(), name='editar_reserva'),
    url(r'^eliminar/reserva/(?P<pk>\d+)/$', EliminarEventosView.as_view(), name='eliminar_reserva')

]
