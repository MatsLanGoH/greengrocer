from django.forms import ModelForm

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from datetime import datetime

from .models import Fruit, Transaction


class FruitForm(ModelForm):
    def clean_label(self):
        data = self.cleaned_data['label']

        # Check label is longer than 1 char
        if len(data) <= 1:
            raise ValidationError(_('商品名は短すぎます。2文字以上で記入してください'))

        # Check label is not longer than 100 chars
        if len(data) > 100:
            raise ValidationError(_('商品名は長すぎます。100文字以内で記入してください'))

        # If all is ok return data
        return data

    def clean_price(self):
        data = self.cleaned_data['price']

        # Check data is an integer
        if not isinstance(data, int):
            raise ValidationError(_('整数を記入してください'))

        # Check that price is not negative
        if data < 0:
            raise ValidationError(_('0円以上の価格を記入してください'))

        # Check that price is not too large
        if data > 1500000:  # 夕張メロンの値段らしい
            raise ValidationError(_('1500000円以下の価格を記入してください'))

        # If all is ok return data
        return data

    def clean_created_at(self):
        data = self.cleaned_data['created_at']

        # Check input is a valid date
        if not isinstance(data, datetime):
            raise ValidationError(_('有効な日付を記入してください'))

        # Check date is not in the future
        if data > timezone.now():
            raise ValidationError(_('未来の日付は記入できません今日までの日付を記入してください。'))

        return data

    class Meta:
        model = Fruit
        fields = ['label', 'price']


class TransactionForm(ModelForm):
    def clean_amount(self):
        data = self.cleaned_data['amount']

        # Check data is an integer
        if not isinstance(data, int):
            raise ValidationError(_('整数を記入してください'))

        # Check amount is not too large
        if data > 1500000000:  # 夕張メロン×1000個分
            raise ValidationError(_('1500000000円以下の価格を記入してください'))

        return data

    def clean_num_items(self):
        data = self.cleaned_data['num_items']

        # Check data is an integer
        if not isinstance(data, int):
            raise ValidationError(_('整数を記入してください'))

        # Check there is at least 1 item in the transaction.
        if data < 1:
            raise ValidationError(_('個数は1個以上を記入してください'))

        # Check not more than 1000 items are being added.
        if data > 1000:
            raise ValidationError(_('個数が多すぎます（1000個以内の数字を記入してください）'))

        return data

    def clean_created_at(self):
        data = self.cleaned_data['created_at']

        # Check input is a valid date
        if not isinstance(data, datetime):
            raise ValidationError(_('有効な日付を記入してください。'))

        # Check date is not in the future
        if data > timezone.now():
            raise ValidationError(_('未来の日付は記入できません。今日までの日付を記入してください。'))

        return data

    class Meta:
        model = Transaction
        fields = ['fruit', 'num_items', 'amount', 'created_at']

