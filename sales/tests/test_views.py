from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from sales.models import Fruit

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
        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('fruits'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('fruits'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'sales/fruit_list.html')

    def test_pagination_is_twenty(self):
        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('fruits'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['fruit_list']) == 20)

    def test_pagination_lists_all_items(self):
        # Get second page and confirm it has exactly 10 remaining items
        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('fruits')+'?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['fruit_list']) == 10)



