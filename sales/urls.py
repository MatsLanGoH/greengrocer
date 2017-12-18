from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

# TODO: add 404 page or standard redirections

urlpatterns = [
    url(r'^$', login_required(views.top), name='top'),
    url(r'^fruits/$', views.FruitListView.as_view(), name='fruits'),
    url(r'^fruit/create/$', views.FruitCreate.as_view(), name='fruit_create'),
    url(r'^fruit/(?P<pk>\d+)/update/$', views.FruitUpdate.as_view(), name='fruit_update'),
    url(r'^fruit/(?P<pk>\d+)/delete/$', views.fruit_delete, name='fruit_delete'),
    url(r'^transactions/$', views.TransactionListView.as_view(), name='transactions'),
    url(r'^transaction/create/$', views.TransactionCreate.as_view(), name='transaction_create'),
    url(r'^transaction/(?P<pk>\d+)/update/$', views.TransactionUpdate.as_view(), name='transaction_update'),
    url(r'^transaction/(?P<pk>\d+)/delete/$', views.transaction_delete, name='transaction_delete'),
    url(r'^upload/csv/$', login_required(views.upload_csv), name='upload_csv'),
    url(r'^stats/$', login_required(views.transaction_stats), name='transaction_stats'),
]
