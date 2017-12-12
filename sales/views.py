from django.contrib.admin.widgets import AdminDateWidget
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.timezone import now
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


def transaction_stats(request):
    """
    TODO: docstring
    :param request:
    :return:
    """
    # TODO: Get Transaction objects
    transactions = Transaction.objects.all()

    # TODO: Total sales
    sum_total = sum([t.amount for t in transactions])

    # TODO: Total past three months with details
    # TODO: Make sure we group same fruit (get set, sort by fruit or something)
    # TODO: Look for edge cases (leap years etc)

    # TODO: Daily sales

    # TODO: Use context to pass data to template
    return render(request,
                  'stats.html',
                  context={
                      'sum_total': sum_total
                  })


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


class TransactionCreate(CreateView):
    # TODO: docstring
    model = Transaction
    fields = ['fruit', 'num_items', 'created_at']
    success_url = reverse_lazy('transactions')
    initial = {'amount': 0,
               'created_at': now()}

    # TODO: Calculate amount from given values (in model)
    def form_valid(self, form):
        # TODO: docstring
        obj = form.save(commit=False)
        obj.amount = obj.fruit.price * obj.num_items
        return super().form_valid(form)

    # TODO: Add a real time picker (jquery or bootstrap)

    # TODO: validate input fields


class TransactionUpdate(UpdateView):
    # TODO: docstring
    model = Transaction
    fields = ['fruit', 'num_items', 'created_at']
    success_url = reverse_lazy('transactions')

    # TODO: validate input fields
    # TODO: make success urls DRY


class TransactionDelete(DeleteView):
    # TODO: docstring
    model = Transaction
    success_url = reverse_lazy('transactions')
