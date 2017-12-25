from django.test import TestCase
from django.utils import timezone

from datetime import timedelta

# Create your tests here.

from sales.models import Fruit
from sales.forms import FruitForm
from sales.forms import TransactionForm


class FruitFormTest(TestCase):

    def test_fruit_form_name_field_label(self):
        form = FruitForm()
        self.assertTrue(form.fields['name'].label is None or form.fields['name'].label == 'Name')

    def test_fruit_form_name_field_help_text(self):
        form = FruitForm()
        self.assertEquals(form.fields['name'].help_text, u"果物の名称を記入してください")

    def test_fruit_form_price_field_label(self):
        form = FruitForm()
        self.assertTrue(form.fields['price'].label is None or form.fields['price'].label == 'Price')

    def test_fruit_form_price_field_help_text(self):
        form = FruitForm()
        self.assertEquals(form.fields['price'].help_text, u"果物の単価を記入してください")

    def test_fruit_form_valid_data(self):
        form_data = {
            'name': 'リンゴ',
            'price': 100
        }
        form = FruitForm(data=form_data)
        self.assertTrue(form.is_valid())
        fruit = form.save()
        self.assertEqual(fruit.name, u"リンゴ")
        self.assertEqual(fruit.price, 100)

    def test_fruit_form_fails_with_invalid_data(self):
        form_data = {
            'name': None,
            'price': None,
        }
        form = FruitForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_fruit_form_name_too_short(self):
        form_data = {'name': 'B'}
        form = FruitForm(data=form_data)
        self.assertTrue(u'商品名は短すぎます。2文字以上で記入してください' in form.errors['name'])

    def test_fruit_form_price_is_not_an_integer(self):
        form_data = {'name': 'リンゴ', 'price': 'one'}
        form = FruitForm(data=form_data)
        self.assertFalse(form.is_valid())


class TransactionFormTest(TestCase):

    def test_transaction_form_valid_data(self):
        fruit_id = Fruit.objects.create(name='リンゴ', price=100)
        cur_date = timezone.now()
        form_data = {
            'fruit': Fruit.objects.last().id,
            'num_items': 10,
            'amount': 1000,
            'created_at': cur_date
        }
        form = TransactionForm(data=form_data)
        self.assertTrue(form.is_valid())
        transaction = form.save()
        self.assertEqual(transaction.fruit, fruit_id)
        self.assertEqual(transaction.num_items, 10)
        self.assertEqual(transaction.amount, 1000)
        self.assertEqual(transaction.created_at, cur_date)

    def test_transaction_for_fails_with_future_date(self):
        Fruit.objects.create(name='リンゴ', price=100)
        cur_date = timezone.now() + timedelta(days=1)
        form_data = {
            'fruit': Fruit.objects.last().id,
            'num_items': 10,
            'amount': 1000,
            'created_at': cur_date
        }
        form = TransactionForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_transaction_for_fails_with_invalid_date(self):
        Fruit.objects.create(name='リンゴ', price=100)
        cur_date = '20120312'
        form_data = {
            'fruit': Fruit.objects.last().id,
            'num_items': 10,
            'amount': 1000,
            'created_at': cur_date
        }
        form = TransactionForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_transaction_for_fails_with_zero_items(self):
        Fruit.objects.create(name='リンゴ', price=100)
        cur_date = timezone.now()
        form_data = {
            'fruit': Fruit.objects.last().id,
            'num_items': 0,
            'amount': 1000,
            'created_at': cur_date
        }
        form = TransactionForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_transaction_for_fails_with_too_many_items(self):
        Fruit.objects.create(name='リンゴ', price=100)
        cur_date = timezone.now()
        form_data = {
            'fruit': Fruit.objects.last().id,
            'num_items': 1001,
            'amount': 1000,
            'created_at': cur_date
        }
        form = TransactionForm(data=form_data)
        self.assertFalse(form.is_valid())
