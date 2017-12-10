from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.top, name='top'),
    url(r'^fruits/$', views.FruitListView.as_view(), name='fruits'),
    url(r'^fruit/create/$', views.FruitCreate.as_view(), name='fruit_create'),
    url(r'^fruit/(?P<pk>\d+)/update/$', views.FruitUpdate.as_view(), name='fruit_update'),
    url(r'^fruit/(?P<pk>\d+)/delete/$', views.FruitDelete.as_view(), name='fruit_delete'),
    url(r'^transactions/$', views.TransactionListView.as_view(), name='transactions'),
    url(r'^transaction/create/$', views.TransactionCreate.as_view(), name='transaction_create'),
    url(r'^transaction/(?P<pk>\d+)/update/$', views.TransactionUpdate.as_view(), name='transaction_update'),
    url(r'^transaction/(?P<pk>\d+)/delete/$', views.TransactionDelete.as_view(), name='transaction_delete'),
    url(r'^stats/$', views.transaction_stats, name='transaction_stats'),
]
