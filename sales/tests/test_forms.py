from django.test import TestCase
from django.core.exceptions import ValidationError

# Create your tests here.

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

    def test_fruit_form_name_too_short(self):
        form_data = {'name': 'B'}
        form = FruitForm(data=form_data)
        self.assertTrue(u'商品名は短すぎます。2文字以上で記入してください' in form.errors['name'])

    """
    def test_fruit_form_name_too_long(self):
        # TODO Fix test
        form_data = {'name': 'B' * 101}
        form = FruitForm(data=form_data)
        self.assertTrue(u'商品名は短すぎます。2文字以上で記入してください' in form.errors['name'])
    """

    def test_fruit_form_price_is_not_an_integer(self):
        form_data = {'name': 'リンゴ', 'price': 'one'}
        form = FruitForm(data=form_data)
        with self.assertRaises(ValidationError):
            form.save()
            form.full_clean()