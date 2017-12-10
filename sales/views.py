from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Fruit, Transaction

# TODO
# TODO: All views need the user to be logged in (except for login site)


# Create views here
def top(request):
    """
    販売管理View（TOP）を返す

    :param request:
    :return:
    """
    # TODO: Add login_required decorator or mixin.
    return render(request,
                  'top.html')


class FruitListView(generic.ListView):
    # TODO: docstring
    model = Fruit

    # TODO: Make sure these are ordered by reverse creation date!
    def get_queryset(self):
        return Fruit.objects.order_by('-created_at')


class FruitCreate(CreateView):
    # TODO: docstring
    model = Fruit
    fields = '__all__'
    success_url = reverse_lazy('fruits')

    # TODO: Validate input number format


class FruitUpdate(UpdateView):
    # TODO: docstring
    model = Fruit
    fields = ['label', 'price']
    success_url = reverse_lazy('fruits')

    # TODO: Validate input number format


class FruitDelete(DeleteView):
    # TODO: docstring
    model = Fruit
    success_url = reverse_lazy('fruits')


class TransactionListView(generic.ListView):
    # TODO: docstring
    model = Transaction

    def get_queryset(self):
        return Transaction.objects.order_by('-created_at')




