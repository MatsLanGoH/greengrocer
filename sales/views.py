from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.forms import HiddenInput
from django.shortcuts import render, reverse, redirect
from django.shortcuts import get_object_or_404
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
    # Transactionレコードを取得する
    transactions = Transaction.objects.all()

    # 1. 累計を計算する
    sum_total = sum([t.amount for t in transactions])

    # レコードはUTCタイムスタンプで登録されているので、集計処理のためローカルタイムゾーン値も取得する
    local_timezone = pytz.timezone(settings.TIME_ZONE)

    # 2. 過去3ヶ月の月別売上情報を集計する
    recent_months = []
    """
    メモ：
    datetime.timedelta()だと日、週の指定はできるが、月はできないが、ワークアラウンドは次の通り。
    今日の年月日を取得し、dayを1に置き換える。
    その日付から、求めるヶ月分×28日を引き、
    取得した年月日のdayを1に置き換える。
    注意：数カ月分だけなら問題ないが、12ヶ月以上の場合、ずれが生じてしまう！
    """
    last_months = [(date.today().replace(day=1) - timedelta(days=_ * 28)).replace(day=1) for _ in range(0, 3)]

    for target_date in last_months:
        # 指定した年月に該当するレコードを選定する
        valid_transactions = []
        for transaction in transactions:
            local_date = local_timezone.normalize(transaction.created_at)
            if (local_date.year, local_date.month) == (target_date.year, target_date.month):
                valid_transactions.append(transaction)

        """
        メモ：
        上記のループ処理は以下のように、lambdaとfilterとして書くことも可能。
        読みづらいのでとりあえず純粋ループで動かす。
        
        valid_transactions = filter(
            lambda t: (local_timezone.normalize(t.created_at).year, local_timezone.normalize(t.created_at).month) == (
                target_date.year, target_date.month), transactions)
        """

        # Ledgerインスタンスを生成し、指定した日付、該当する販売情報を登録する
        ledger = Ledger(target_date, valid_transactions)

        # 過去販売情報のリストにLedgerを加える。
        recent_months.append(ledger)

    # 3. 過去3ヶ日の日別売上情報を集計する
    recent_days = []
    last_days = [date.today() - timedelta(days=_) for _ in range(0, 3)]

    for target_date in last_days:
        # 指定した年月日に該当するレコードを選定する
        valid_transactions = filter(lambda t: local_timezone.normalize(t.created_at).date() == target_date,
                                    transactions)

        # Ledgerインスタンスを生成し、指定した日付、該当する販売情報を登録する
        ledger = Ledger(target_date, valid_transactions)

        # 過去販売情報のリストにLedgerを加える。
        recent_days.append(ledger)

    return render(request,
                  'stats.html',
                  context={
                      'sum_total': sum_total,
                      'recent_months': recent_months,
                      'recent_days': recent_days,
                  })


@login_required
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

        # ファイルの検証
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

        count_success = 0  # 成功したアップロードのカウント
        count_fail = 0  # 失敗したアップロードのカウント

        # 販売情報をdbに登録する
        for line in lines:
            fields = line.split(',')
            # try:
            t = Transaction()
            t.fruit = Fruit.objects.get(label=fields[0])
            t.num_items = fields[1]
            t.amount = fields[2]
            t.created_at = fields[3]
            # TODO: don't forget to set tzinfo as well (handler is complaining already)
            t.save()
            count_success += 1
            # except Exception as e:
            # TODO: Improve exception handling
            # count_fail += 1


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
    paginate_by = 20

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


@login_required
def fruit_delete(request, pk):
    """
    Fruitを削除する
    :param request:
    :param pk: Fruitのプライマリーキー
    :return: Fruit 一覧に戻る
    """
    fruit = get_object_or_404(Fruit, pk=pk)
    fruit.delete()
    return HttpResponseRedirect(reverse('fruits'))


class TransactionListView(LoginRequiredMixin, generic.ListView):
    """
    Transaction 一覧を表示するView
    """
    model = Transaction
    paginate_by = 20

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
        """
        フォーム送信時に販売情報の合計金額を計算し、レコードを登録する
        :param form:
        :return:
        """
        if form.is_valid():
            obj = form.save(commit=False)
            obj.amount = obj.fruit.price * obj.num_items
            return super().form_valid(form)


class TransactionUpdate(LoginRequiredMixin, TransactionMixin, UpdateView):
    """
    Transaction編集のView
    """
    # fields = ['fruit', 'num_items', 'amount', 'created_at']
    pass


@login_required
def transaction_delete(request, pk):
    """
    Transactionを削除する
    :param request:
    :param pk: Transactionのプライマリーキー
    :return: Transaction 一覧に戻る
    """
    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.delete()
    return HttpResponseRedirect(reverse('transactions'))


def handler404(request):
    return redirect('top')
