from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
from .forms import *
from .views import *

class ModelsTestCase(TestCase):
    def test_user_profile_creation(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        user_profile = UserProfile.objects.create(user=user)
        self.assertEqual(user_profile.name, '')

    def test_user_profile_str_method(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        user_profile = UserProfile.objects.create(user=user, name='Test Name', email='test@example.com')
        self.assertEqual(str(user_profile), 'testuser')

class FormsTestCase(TestCase):
    def test_register_form(self):
        form_data = {'username': 'testuser', 'email': 'test@example.com', 'password1': 'testpassword', 'password2': 'testpassword'}
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_form_invalid_data(self):
        form_data = {'username': '', 'email': 'invalid_email', 'password1': 'password', 'password2': 'password'}
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password2', form.errors)

    # ... (existing tests)

    def test_register_form_invalid_data(self):
        form_data = {'username': '', 'email': 'invalid_email', 'password1': 'password', 'password2': 'password'}
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password2', form.errors)

    def test_new_expense_form_valid_data(self):
        form_data = {'name': 'Test Name', 'amount': 50.0, 'category': 'Groceries', 'notes': 'Test Expense'}
        form = NewExpenseForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_new_expense_form_valid_data(self):
        form_data = {'name': 'Test Name', 'amount': 50.0, 'category': 'Groceries', 'notes': 'Test Expense'}
        form = NewExpenseForm(data=form_data)
        self.assertTrue(form.is_valid())


class ViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_sign_up_view(self):
        response = self.client.get(reverse('sign_up'))
        self.assertEqual(response.status_code, 200)

    def test_expense_list_view(self):
        response = self.client.get(reverse('expense_list'))
        self.assertEqual(response.status_code, 200)

    def test_add_expense_view(self):
        response = self.client.get(reverse('add_expense'))
        self.assertEqual(response.status_code, 200)

    def test_delete_expense_view(self):
        response = self.client.get(reverse('delete_expense', args=[999]))  # 999 is a placeholder for a non-existent expense ID
        self.assertEqual(response.status_code, 404)

    def test_modify_expense_view(self):
        response = self.client.get(reverse('modify_expense', args=[999]))  # 999 is a placeholder for a non-existent expense ID
        self.assertEqual(response.status_code, 404)

    def test_home_view_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_sign_up_view_template(self):
        response = self.client.get(reverse('sign_up'))
        self.assertTemplateUsed(response, 'registration/sign_up.html')

    def test_expense_list_view_template(self):
        response = self.client.get(reverse('expense_list'))
        self.assertTemplateUsed(response, 'no_expenses.html')

    def test_add_expense_view_template(self):
        response = self.client.get(reverse('add_expense'))
        self.assertTemplateUsed(response, 'add_expense.html')

    def test_user_input_name_view_template(self):
        response = self.client.get(reverse('user_input_name'))
        self.assertTemplateUsed(response, 'input_name.html')

    # ... (existing tests)

    def test_home_view_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_sign_up_view_template(self):
        response = self.client.get(reverse('sign_up'))
        self.assertTemplateUsed(response, 'registration/sign_up.html')

    def test_add_expense_view_template(self):
        response = self.client.get(reverse('add_expense'))
        self.assertTemplateUsed(response, 'add_expense.html')

    def test_user_input_name_view_template(self):
        response = self.client.get(reverse('user_input_name'))
        self.assertTemplateUsed(response, 'input_name.html')


class URLsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        UserProfile.objects.create(user=self.user)
        self.client.login(username='testuser', password='testpassword')

    def test_home_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_sign_up_url(self):
        response = self.client.get('/sign-up/')
        self.assertEqual(response.status_code, 200)

    def test_expense_list_url(self):
        response = self.client.get('/expenses/')
        self.assertEqual(response.status_code, 200)

    def test_add_expense_url(self):
        response = self.client.get('/expenses/add-expense/')
        self.assertEqual(response.status_code, 200)

    def test_modify_expense_url(self):
        response = self.client.get(reverse('modify_expense', args=[999]))  # 999 is a placeholder for a non-existent expense ID
        self.assertEqual(response.status_code, 404)

    def test_delete_expense_url(self):
        response = self.client.get(reverse('delete_expense', args=[999]))  # 999 is a placeholder for a non-existent expense ID
        self.assertEqual(response.status_code, 404)

    def test_user_input_name_url(self):
        response = self.client.post(reverse('user_input_name'), {'name': 'Test'})
        self.assertEqual(response.status_code, 302)  # Assuming the view redirects
        # Assuming your view sets a 'url' variable before redirecting
        if response.url:
            self.assertTrue(response.url.startswith('/'))  # Ensure it's a relative URL
        else:
            self.fail('URL not found in the response.')

