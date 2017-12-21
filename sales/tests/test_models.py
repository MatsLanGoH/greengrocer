from django.test import TestCase

# Create your tests here.
from sales.models import Fruit
from sales.models import Transaction

from django.utils import timezone


class FruitModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods.
        Fruit.objects.create(name='リンゴ', price=100)

    def test_name_label(self):
        fruit = Fruit.objects.get(id=1)
        field_label = fruit._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_price_label(self):
        fruit = Fruit.objects.get(id=1)
        field_label = fruit._meta.get_field('price').verbose_name
        self.assertEquals(field_label, 'price')

    def test_name_max_length(self):
        fruit = Fruit.objects.get(id=1)
        max_length = fruit._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)

    def test_object_name_is_name_and_price(self):
        fruit = Fruit.objects.get(id=1)
        expected_object_name = "{} (単価：{})".format(fruit.name, fruit.price)
        self.assertEquals(expected_object_name, str(fruit))


class TransactionModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods.
        Fruit.objects.create(name='リンゴ', price=100)
        fruit = Fruit.objects.get(id=1)
        Transaction.objects.create(fruit=fruit, num_items=10, amount=1000, created_at=timezone.now())

    def test_fruit_label(self):
        transaction = Transaction.objects.get(id=1)
        field_label = transaction._meta.get_field('fruit').verbose_name
        self.assertEquals(field_label, 'fruit')

    def test_num_items_label(self):
        transaction = Transaction.objects.get(id=1)
        field_label = transaction._meta.get_field('num_items').verbose_name
        self.assertEquals(field_label, 'num items')

    def test_amount_label(self):
        transaction = Transaction.objects.get(id=1)
        field_label = transaction._meta.get_field('amount').verbose_name
        self.assertEquals(field_label, 'amount')

    def test_created_at_label(self):
        transaction = Transaction.objects.get(id=1)
        field_label = transaction._meta.get_field('created_at').verbose_name
        self.assertEquals(field_label, 'created at')

    def test_object_name_is_fruit_name_amount_and_num_items(self):
        transaction = Transaction.objects.get(id=1)
        expected_object_name = "{}: {}円({})".format(transaction.fruit.name, transaction.amount, transaction.num_items)
        self.assertEquals(expected_object_name, str(transaction))
