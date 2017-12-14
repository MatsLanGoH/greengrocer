from django.contrib import messages
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Fruit, Transaction

from datetime import datetime, date, timedelta
import pytz

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


class TransactionStat(object):
    """
    TODO: docstring
    this should hold all transactions for that date.
    """

    def __init__(self):
        self.date = date.today()
        self.total = 0  # TODO: Get amount from items instead
        self.transactions = dict()

    def update_total(self):
        """
        TODO docstring
        :return:
        """
        total = 0
        for item in self.transactions.values():
            total += item.amount
        self.total = total

    def __str__(self):
        """
        TODO docstring
        :return:
        """
        msg = ""
        for fruit, transaction in self.transactions.items():
            msg += "{fruit}: {amount}円({num_items}) ".format(fruit=fruit.label, amount=transaction.amount,
                                                             num_items=transaction.num_items)
        return msg


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
    recent_months = []

    local_timezone = pytz.timezone('Asia/Tokyo')

    # TODO: the next line is super confusing. works though.
    last_months = [(date.today().replace(day=1) - timedelta(days=_ * 28)).replace(day=1) for _ in range(0, 3)]

    for target_date in last_months:
        # Create a new TransactionStat instance for the target date.
        t_stat = TransactionStat()
        t_stat.date = target_date

        # Find all valid transactions for the target date.
        valid_transactions = []
        for transaction in transactions:
            local_date = local_timezone.normalize(transaction.created_at)
            if (local_date.year, local_date.month) == (target_date.year, target_date.month):
                valid_transactions.append(transaction)

        # Summarize transaction stats (num of sold items, amount) into TransactionStat instance
        for transaction in valid_transactions:
            if transaction.fruit in t_stat.transactions.keys():
                t_stat.transactions[transaction.fruit].num_items += transaction.num_items
                t_stat.transactions[transaction.fruit].amount += transaction.amount

            else:
                t_stat.transactions[transaction.fruit] = transaction

        # Finally, update total amount and add TransactionStat to list
        t_stat.update_total()
        recent_months.append(t_stat)

    # TODO: Daily sales
    recent_days = []

    last_days = [date.today() - timedelta(days=_) for _ in range(0, 3)]

    for target_date in last_days:
        # Create a new TransactionStat instance for the target date.
        t_stat = TransactionStat()
        t_stat.date = target_date

        # Find all valid transactions for the target date.
        valid_transactions = []
        for transaction in transactions:
            local_date = local_timezone.normalize(transaction.created_at)
            if local_date.date() == target_date:
                valid_transactions.append(transaction)

        # Summarize transaction stats (num of sold items, amount) into TransactionStat instance
        for transaction in valid_transactions:
            if transaction.fruit in t_stat.transactions.keys():
                t_stat.transactions[transaction.fruit].num_items += transaction.num_items
                t_stat.transactions[transaction.fruit].amount += transaction.amount
            else:
                t_stat.transactions[transaction.fruit] = transaction

        # Finally, update total amount and add TransactionStat to list
        t_stat.update_total()
        recent_days.append(t_stat)

    # TODO: Use context to pass data to template
    return render(request,
                  'stats.html',
                  context={
                      'sum_total': sum_total,
                      'recent_months': recent_months,
                      'recent_days': recent_days,
                  })

def upload_csv(request):
    # TODO: docstring
    if request.method == "GET":
        # TODO: Use url redirection
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
            print(line)
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
                count_fail += 1
                # TODO: Fix exception handling
                print(fields)
                print(e)

            # TODO: Reimplement this using forms
            # http: // thepythondjango.com / upload - process - csv - file - django /

        messages.error(request, 'CSV一括登録結果 (成功:{}件　失敗:{}件)'.format(count_success, count_fail))
    except Exception as e:
        # TODO: Fix exception handling
        print(e)

    # TODO: Use url redirection
    return HttpResponseRedirect(reverse('transactions'))


class FruitListView(generic.ListView):
    # TODO: docstring
    model = Fruit
    paginate_by = 30

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
    paginate_by = 30

    def get_queryset(self):
        return Transaction.objects.order_by('-created_at')


class TransactionCreate(CreateView):
    # TODO: docstring
    model = Transaction
    fields = ['fruit', 'num_items', 'created_at']
    success_url = reverse_lazy('transactions')
    initial = {'amount': 0,
               'created_at': datetime.now()}
    # TODO: datetime.now() stops at server start time

    # TODO: Calculate amount from given values (in model)
    def form_valid(self, form):
        # TODO: docstring
        obj = form.save(commit=False)
        obj.amount = obj.fruit.price * obj.num_items
        return super().form_valid(form)

    # TODO: validate input fields


class TransactionUpdate(UpdateView):
    # TODO: docstring
    model = Transaction
    fields = ['fruit', 'num_items', 'created_at']
    success_url = reverse_lazy('transactions')

    # TODO: Should UpdateView have different fields? Users might have to fix everything!
    # TODO: validate input fields
    # TODO: make success urls DRY


class TransactionDelete(DeleteView):
    # TODO: docstring
    model = Transaction
    success_url = reverse_lazy('transactions')
