from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.top, name='top'),
    url(r'^fruits/$', views.FruitListView.as_view(), name='fruits'),
    url(r'^fruit/create/$', views.FruitCreate.as_view(), name='fruit_create'),
    url(r'^fruit/(?P<pk>\d+)/update/$', views.FruitUpdate.as_view(), name='fruit_update'),
    url(r'^fruit/(?P<pk>\d+)/delete/$', views.FruitDelete.as_view(), name='fruit_delete'),
    url(r'^transactions/$', views.TransactionListView.as_view(), name='transactions'),
]
