from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import HiddenInput
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

import pytz
from datetime import datetime, date, timedelta

from .forms import FruitForm, TransactionForm
from .models import Fruit, Transaction
from .ledger import Ledger


# Create views here
def top(request):
    """
    販売管理View（TOP）を返す

    :param request:
    :return:
    """
    return render(request,
                  'top.html')


def transaction_stats(request):
    """
    販売統計情報を生成するView

    :param request:
    :return:
    """
    # Get Transaction objects
    transactions = Transaction.objects.all()

    # Get local timezone to adjust UTC timestamps inside database objects
    local_timezone = pytz.timezone(settings.TIME_ZONE)

    # 1. Calculate total sales
    sum_total = sum([t.amount for t in transactions])

    # 2. Get details for past three months
    # TODO: Total past three months with details
    recent_months = []
    # TODO: the next line is super confusing. works though.
    last_months = [(date.today().replace(day=1) - timedelta(days=_ * 28)).replace(day=1) for _ in range(0, 3)]

    for target_date in last_months:
        # Find all valid transactions for the target date.
        valid_transactions = []
        for transaction in transactions:
            local_date = local_timezone.normalize(transaction.created_at)
            if (local_date.year, local_date.month) == (target_date.year, target_date.month):
                valid_transactions.append(transaction)

        # Todo: Lambda works, but is hard to understand.
        valid_transactions = filter(
            lambda t: (local_timezone.normalize(t.created_at).year, local_timezone.normalize(t.created_at).month) == (
                target_date.year, target_date.month), transactions)

        # Create a new Ledger instance for the target date.
        ledger = Ledger()
        ledger.set_date(target_date)
        ledger.add_transactions(valid_transactions)

        # Finally, update total amount and add Ledger to list
        ledger.update_total()

        recent_months.append(ledger)

    # 3. Get sales for past three days
    # TODO: Daily sales
    recent_days = []
    last_days = [date.today() - timedelta(days=_) for _ in range(0, 3)]

    for target_date in last_days:
        # Find all valid transactions for the target date.
        valid_transactions = filter(lambda t: local_timezone.normalize(t.created_at).date() == target_date,
                                    transactions)

        # Create a new Ledger instance for the target date.
        ledger = Ledger()
        ledger.set_date(target_date)
        ledger.add_transactions(valid_transactions)

        # Finally, update total amount and add Ledger to list
        ledger.update_total()

        recent_days.append(ledger)

    # TODO: Use context to pass data to template
    return render(request,
                  'stats.html',
                  context={
                      'sum_total': sum_total,
                      'recent_months': recent_months,
                      'recent_days': recent_days,
                  })


def upload_csv(request):
    """
    CSV一括登録用のView

    :param request:
    :return:
    """
    if request.method == "GET":
        return HttpResponseRedirect(reverse('transactions'))

    try:
        csv_file = request.FILES['csv_file']
        # TODO: File validation
        # File doesn't end with .csv
        if not csv_file.name.endswith('.csv'):
            messages.error(request, '参照したファイルはCSV形式ではありません')
            return HttpResponseRedirect(reverse('transactions'))
        # File is too large
        if csv_file.multiple_chunks():
            messages.error(request, '参照ファイルは大きすぎます(%.2f MB)' % (csv_file.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse('transactions'))

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split('\n')

        count_success = 0
        count_fail = 0

        # Loop over lines and try to store Transactions in db.
        for line in lines:
            fields = line.split(',')
            try:
                t = Transaction()
                t.fruit = Fruit.objects.get(label=fields[0])
                t.num_items = fields[1]
                t.amount = fields[2]
                t.created_at = fields[3]
                # TODO: don't forget to set tzinfo as well (handler is complaining already)
                t.save()
                count_success += 1
            except Exception as e:
                # TODO: Improve exception handling
                count_fail += 1

            # TODO: Reimplement this using forms
            # http: // thepythondjango.com / upload - process - csv - file - django /

        messages.error(request, 'CSV一括登録結果 (成功:{}件　失敗:{}件)'.format(count_success, count_fail))
    except Exception as e:
        # TODO: Improve exception handling
        print(e)

    return HttpResponseRedirect(reverse('transactions'))


class FruitListView(LoginRequiredMixin, generic.ListView):
    """
    Fruit 一覧を表示するView
    """
    model = Fruit
    paginate_by = 30

    def get_queryset(self):
        return Fruit.objects.order_by('-created_at')


class FruitMixin(object):
    model = Fruit
    form_class = FruitForm
    success_url = reverse_lazy('fruits')


class FruitCreate(LoginRequiredMixin, FruitMixin, CreateView):
    """
    Fruit 登録のView
    """
    pass


class FruitUpdate(LoginRequiredMixin, FruitMixin, UpdateView):
    """
    Fruit 編集のView
    """
    pass


class FruitDelete(LoginRequiredMixin, FruitMixin, DeleteView):
    """
    Fruit 削除のView
    """
    pass


class TransactionListView(LoginRequiredMixin, generic.ListView):
    """
    Transaction 一覧を表示するView
    """
    model = Transaction
    paginate_by = 30

    def get_queryset(self):
        return Transaction.objects.order_by('-created_at')


class TransactionMixin(object):
    model = Transaction
    form_class = TransactionForm
    success_url = reverse_lazy('transactions')


class TransactionCreate(LoginRequiredMixin, TransactionMixin, CreateView):
    """
    Transaction新規登録のView
    """
    # TODO: Can we remove this line? Or move it into our Form definition
    initial = {'amount': 0,
               'created_at': datetime.now}

    def get_form(self, form_class=None):
        form = super(TransactionCreate, self).get_form()
        form.fields['amount'].widget = HiddenInput()
        return form

    def form_valid(self, form):
        # TODO: docstring
        obj = form.save(commit=False)
        # TODO: Calculate amount from given values (in model)
        obj.amount = obj.fruit.price * obj.num_items
        return super().form_valid(form)


class TransactionUpdate(LoginRequiredMixin, TransactionMixin, UpdateView):
    """
    Transaction編集のView
    """
    # fields = ['fruit', 'num_items', 'amount', 'created_at']
    pass


class TransactionDelete(LoginRequiredMixin, TransactionMixin, DeleteView):
    """
    Transaction削除のView
    """
    pass
