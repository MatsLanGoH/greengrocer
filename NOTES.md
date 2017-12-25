# greengrocer
Sales tracker application written in Django 
(Demo at [pythonanywhere](https://matslangoh.pythonanywhere.com) / login: testuser / pw: playground)

# Getting started.
  - clone this repository: `git clone https://github.com/matslangoh/greengrocer`
  - create and activate virtual environment with Python 3.5+: `python3 -m venv env`, `. env/bin/activate` (or similar)
  - install requirements: `pip install -r requirements.txt`
  - prepare db: `python manage.py makemigrations && python manage.py migrate`
  - create a superuser: `python manage.py createsuperuser`
  - and finally run the server: `python manage.py runserver` (with `--insecure` flag if you don't have a server for static files)


# 全般の工夫点

## 環境設定
- `settings.py` → 本来であればDevelopment、Productionなどに分けるが、ローカルで動かすことがメインとなるためほとんど変更していません。
- SECRET_KEYはそのままになっているが、本来であれば環境もしくは別ファイルで設定し、os.environで読み込む。
- STATIC_FILESについては、ローカルだけで動かしているので、`DEBUG = False`の場合は`python manage.py runserver --insecure`で起動する。


## フロントエンド
- Bootstrap 3を使用しているため、モバイルデバイスでの表示にも対応している。
- Djangoフォームの標準設定ではBootstrapが組み込みづらいため、`django-widget-tweaks`パッケージを使用し、ラベル・フィールドのカスタムデザインを加えた。
```
# example
{% load widget_tweaks %}
<form action="" method="post" class="form-horizontal">
{% csrf_token %}
<div class="form-group">
    <label class="col-md-4 control-label" for="{{ form.name.id_for_name }}">名称</label>
    <div class="col-md-4">
        {% render_field form.name class+="form-control" %}
    </div>
    {% for error in form.name.errors %}
        <p class="text-warning">{{ error }}</p>
    {% endfor %}
</div>
```

# Views

## ログイン画面
- Django標準の認証システムを運用している。ユーザ登録機能は実装していないため、`python manage.py createsuperuser`でSuperuserを登録し、他のユーザアカウントが必要な場合はDjango Adminから登録する。
- ログインエラー（ユーザ名、パスワードなど）はログインフォームに表示される。
- ログインしていない場合、強制的にこのページにリダイレクトされる。
- 存在していないページからリダイレクトされた場合も、ログイン画面の下にエラーメッセージが表示される。(`django.contrib.messages`を利用している)

## Top画面
 - おおむね仕様説明に基づいて作成したが、右上にログアウトボタンを追加した。
 - ログイン済みのユーザは、404/500エラーが生じた場合このページにリダイレクトされる。その際、ページの下にエラーメッセージが表示される。
 - リンクは原則、`urls.py`で指定し、`{% url 'hoge' %}`としてテンプレートに埋め込んだ。
 ```
 class FruitListView(LoginRequiredMixin, generic.ListView):
    """
    Fruit 一覧を表示するView
    """
    model = Fruit
    paginate_by = 20

    def get_queryset(self):
        return Fruit.objects.order_by('-updated_at')


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
 ```
 

## 商品マスタ管理
  - 操作等は仕様説明の通りに動く。
  - 一覧は`django.views.generic.ListView`、登録／編集画面は`CreateView`, `EditView`を使用した。Mixinを使用することによって、重複なく構築している。
  - 単純なページネーションはページ下部分につけてある（レコードが20件を超えた場合表示される）
  - ログイン条件はそれぞれ`@login_required`, `LoginRequiredMixin`でチェックしている。


## 販売情報管理
  - 操作等は仕様説明の通りに動く。
  - 基本的な表示科目は商品マスタ管理と同様に実装している。
  - CSV一括アップロードは、フロントエンドの方でファイル名末尾が`.csv`であればアップロードボタンが有効になる（jQuery）。
  ```
      <script>
        // Show filename in form text
        $(document).on('change', ':file', function () {
            var input = $(this),
                label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
            input.parent().parent().next(':text').val(label);
            if (label.includes(".csv")) {
                $('#csvFileSelect').toggleClass('btn-primary');
                $('#csvButton').prop('disabled', false)
                    .addClass('btn-success');
            }
        });
    </script>
  ```

  - Viewのコードで、同様にファイル名末尾のチェック、ファイルサイズが大きすぎないかをチェックし、一行ごとに販売情報をレコードに登録する。[How to upload and process the CSV file in Django](http://thepythondjango.com/upload-process-csv-file-django/)
  
  ```
        # ファイル名末尾はCSVかチェックする
        if not csv_file.name.endswith('.csv'):
            messages.error(request, '参照したファイルはCSV形式ではありません')
            return HttpResponseRedirect(reverse('transactions'))

        # ファイルサイズは大きすぎないかチェックする
        if csv_file.multiple_chunks():
            messages.error(request, '参照ファイルは大きすぎます(%.2f MB)' % (csv_file.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse('transactions'))
  ```
  
  - 正常に登録できなかったレコード以外は`pass`していく。（`except Exception as e:`としているが、本当はアンチパターンを避けてもう少し丁寧に処理した方が良いかもしれない。）



## 商品＆販売情報登録／編集フォーム
  - 操作等は仕様説明の通りに動く。
  - 各項目の必須形式チェック、モデルで指定されているため無効な値は登録できないようになっている。
  - 他に問題になりそうな記入値（例えば商品名が短すぎる、長すぎる、個数が多すぎる、価格が高すぎる）については`forms.py`でチェックしている。
  ```
      # example
      def clean_created_at(self):
        data = self.cleaned_data['created_at']

        # Check input is a valid date
        if not isinstance(data, datetime):
            raise ValidationError(_('有効な日付を記入してください'))

        # Check date is not in the future
        if data > timezone.now():
            raise ValidationError(_('未来の日付は記入できません。今日までの日付を記入してください。'))

        return data
  ```
  
  - 販売情報登録フォームの仕様説明では「売り上げ」を指定しないことになっているため、フォーム送信時に商品の単価と個数から計算し、登録する仕組みを実装した。編集画面については、全項目が編集できるようになっている。
  ```
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
  ```


## 商品販売管理
  - 仕様説明の通り、Django ORMを利用せず実装した。
  - 詳細は次の通り。
  - *累計*はDBより販売情報を全レコード取得し、`amount`を集計する。(累計だけ必要であれば、`Transaction.objects.all()`ではなくて、`Transactions.objects.value('amount')`を使うが、月別・日別の時にもレコードが必要なため`all`のまま)
  
  ```
    transactions = Transaction.objects.all()
    sum_total = sum([t.amount for t in transactions])
  ```
  
  - **月別・日別**は基本的に似ているが、選定が妙に違う。現時点の日付を取得し`timedelta`を使用し、過去3ヶ月（3日間）の年月日をリストに加えていく。月別も「日」まで指定するが、その日を「１」とし、同じ月に発生した販売レコードをすべて集計する。
  
  - 過去3日間の機能は問題なく動いているが、過去3ヶ月の実装には致命的欠点がある。`timedelta`は◯ヶ月単位のdeltaを指定できないが、年始→年末を指定するのに便利（ex. 2017-01-01 - timedelta(days=1）=> 2016-12-31）なので、月単位にも使用したかった。3ヶ月という期間では実際問題ないが、長期間のデータ表示が必要な場合は使えなくなってしまうため、その際は`dateutil`パッケージを使っているか、より丁寧に月の日数を示すロジックを書く必要がある。
  
  ```
    """
    メモ：
    datetime.timedelta()だと日、週の指定はできるが、月はできないが、ワークアラウンドは次の通り。
    今日の年月日を取得し、dayを1に置き換える。
    その日付から、求めるヶ月分×28日を引き、
    取得した年月日のdayを1に置き換える。
    注意：数カ月分だけなら問題ないが、12ヶ月以上の場合、ずれが生じてしまう！
    """
    last_months = [(date.today().replace(day=1) - timedelta(days=_ * 28)).replace(day=1) for _ in range(0, 3)]
  ```
  
  - リストに加えた日付に沿って、該当する販売登録を別のリストに保存していく。`Transaction`レコードでは基本的に商品一つしか登録できないため、複数の商品×個数を集計する`Ledger`クラスを別に作成した。`Ledger`は`datetime`と`dict`を所有し、指定された日付に合う販売情報をインスタンスの辞書に集約することができる。（Viewでしか必要ないため、モデルではなくクラスとして実装した）。
  
  ```
  # Ledgerインスタンスを生成し、指定した日付、該当する販売情報を登録する
  ledger = Ledger(target_date, valid_transactions)
  ```
  
  ```
  class Ledger:
    """
    販売情報を登録し、合計金額、売上、内訳を返すためのクラス
    """

    def __init__(self, ledger_date=date.today(), transactions=None):
        """
        :param ledger_date: まとめる販売情報の年月日
        :param transactions: Ledgerクラスにまとめる販売情報（Transactionレコード）
        """
        self.ledger_date = ledger_date
        self.total = 0
        self.transactions = dict()

        if transactions:
            self.add_transactions(transactions)
            self.update_total()
    ```

## 単体テスト
  - 一通り、基本的なテストを実装し、それぞれ仕様説明にあるCHECK条件を満たしていることだけ確認している。
  
