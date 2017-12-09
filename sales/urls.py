from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.top, name='top'),
    url(r'^fruits/$', views.FruitListView.as_view(), name='fruits'),
    url(r'^salesledgers/$', views.SalesLedgerListView.as_view(), name='salesledgers'),
]
