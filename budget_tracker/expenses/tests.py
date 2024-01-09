from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
from .forms import *
from .views import *


class ModelsTestCase(TestCase):
    def test_user_profile_creation(self):
        """
        Test the creation of a user profile.

        Creates a user and a corresponding user profile.
        Checks if the user profile's name field is empty.

        """
        user = User.objects.create_user(username='testuser', password='testpassword')
        user_profile = UserProfile.objects.create(user=user)
        self.assertEqual(user_profile.name, '')

    def test_user_profile_str_method(self):
        """
        Test the string representation of a user profile.

        Creates a user and a corresponding user profile with specified name and email.
        Checks if the string representation matches the expected username.

        """
        user = User.objects.create_user(username='testuser', password='testpassword')
        user_profile = UserProfile.objects.create(user=user, name='Test Name', email='test@example.com')
        self.assertEqual(str(user_profile), 'testuser')

class FormsTestCase(TestCase):
    def test_register_form(self):
        """
        Test the registration form validation.

        Creates a registration form with valid data and asserts its validity.

        """
        form_data = {'username': 'testuser', 'email': 'test@example.com', 'password1': 'testpassword', 'password2': 'testpassword'}
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_form_invalid_data(self):
        """
        Test the registration form with invalid data.

        Creates a registration form with invalid data and asserts its invalidity.
        Checks for specific errors in the form.

        """
        form_data = {'username': '', 'email': 'invalid_email', 'password1': 'password', 'password2': 'password'}
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password2', form.errors)

    def test_new_expense_form_valid_data(self):
        """
        Test the new expense form with valid data.

        Creates a new expense form with valid data and asserts its validity.

        """
        form_data = {'name': 'Test Name', 'amount': 50.0, 'category': 'Groceries', 'notes': 'Test Expense'}
        form = NewExpenseForm(data=form_data)
        self.assertTrue(form.is_valid())

class ViewsTestCase(TestCase):
    def setUp(self):
        """
        Set up a user and login for view tests.

        Creates a user and logs in using the client.

        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_home_view(self):
        """
        Test the home view.

        Sends a GET request to the home view and checks for a successful response.

        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_sign_up_view(self):
        """
        Test the sign-up view.

        Sends a GET request to the sign-up view and checks for a successful response.

        """
        response = self.client.get(reverse('sign_up'))
        self.assertEqual(response.status_code, 200)

    # ... (additional view tests)

    def test_user_input_name_view_template(self):
        """
        Test the user input name view template.

        Sends a GET request to the user input name view and checks if the correct template is used.

        """
        response = self.client.get(reverse('user_input_name'))
        self.assertTemplateUsed(response, 'input_name.html')

class URLsTestCase(TestCase):
    def setUp(self):
        """
        Set up a user and login for URL tests.

        Creates a user and logs in using the client.

        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        UserProfile.objects.create(user=self.user)
        self.client.login(username='testuser', password='testpassword')

    def test_home_url(self):
        """
        Test the home URL.

        Sends a GET request to the home URL and checks for a successful response.

        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_sign_up_url(self):
        """
        Test the sign-up URL.

        Sends a GET request to the sign-up URL and checks for a successful response.

        """
        response = self.client.get('/sign-up/')
        self.assertEqual(response.status_code, 200)

    # ... (additional URL tests)

    def test_user_input_name_url(self):
        """
        Test the user input name URL.

        Sends a POST request to the user input name URL and checks for a redirection.

        """
        response = self.client.post(reverse('user_input_name'), {'name': 'Test'})
        self.assertEqual(response.status_code, 302)  # Assuming the view redirects
        # Assuming your view sets a 'url' variable before redirecting
        if response.url:
            self.assertTrue(response.url.startswith('/'))  # Ensure it's a relative URL
        else:
            self.fail('URL not found in the response.')
