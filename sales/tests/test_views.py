from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from sales.models import Fruit, Transaction

from datetime import timedelta


# Create your tests here.


class FruitListViewTest(TestCase):

    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1')
        test_user1.set_password('12345')
        test_user1.save()

    @classmethod
    def setUpTestData(cls):
        # Create 30 types of fruit for pagination tests
        number_of_fruits = 30
        for fruit_num in range(number_of_fruits):
            Fruit.objects.create(name='Fruit %s' % fruit_num, price=100)

    def test_view_redirects_to_top_when_not_logged_in(self):
        resp = self.client.get(reverse('fruits'))
        self.assertEqual(resp.status_code, 302)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('fruits'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('fruits'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'sales/fruit_list.html')

    def test_pagination_is_twenty(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('fruits'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['fruit_list']) == 20)

    def test_pagination_lists_all_items(self):
        # Get second page and confirm it has exactly 10 remaining items
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('fruits') + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['fruit_list']) == 10)


class TransactionListViewTest(TestCase):

    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1')
        test_user1.set_password('12345')
        test_user1.save()

    @classmethod
    def setUpTestData(cls):
        # Create 3 types of fruit
        number_of_fruits = 30
        for fruit_num in range(number_of_fruits):
            Fruit.objects.create(name='Fruit %s' % fruit_num, price=100)

        # Create 30 types of Transaction for pagination tests
        number_of_transactions = 30
        for transaction_num in range(number_of_transactions):
            fruit = Fruit.objects.get(id=transaction_num + 1)
            Transaction.objects.create(fruit=fruit, num_items=transaction_num, amount=transaction_num * 100,
                                       created_at=timezone.now() - timedelta(
                                           days=number_of_transactions - transaction_num))

    def test_view_redirects_to_top_when_not_logged_in(self):
        resp = self.client.get(reverse('transactions'))
        self.assertEqual(resp.status_code, 302)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('transactions'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('transactions'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'sales/transaction_list.html')

    def test_pagination_is_twenty(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('transactions'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['transaction_list']) == 20)

    def test_pagination_lists_all_items(self):
        # Get second page and confirm it has exactly 10 remaining items
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('transactions') + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['transaction_list']) == 10)


