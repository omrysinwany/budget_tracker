# forms.py

from datetime import date
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm as BasePasswordChangeForm
from django.contrib.auth.models import User
from .models import Expense, UserProfile

class UserInput(forms.Form):
    """
    A form for user input, specifically for choosing from unique expense names.

    Methods:
    - __init__: Initializes the form with choices based on unique expense names for a specific user.
    """
    def __init__(self, user, *args, **kwargs):
        super(UserInput, self).__init__(*args, **kwargs)
        unique_names_set = set(Expense.objects.filter(user__user=user).values_list('name', flat=True).distinct())
        self.fields['name'] = forms.ChoiceField(choices=[(name, name) for name in unique_names_set])

class NewExpenseForm(forms.Form):
    """
    A form for creating a new expense.

    Fields:
    - name: The name or description of the expense.
    - amount: The amount of the expense.
    - category: The category of the expense (selectable from predefined choices).
    - notes: Additional notes related to the expense (optional).

    Methods:
    - clean_name: Capitalizes the name input.
    - clean_category: Capitalizes the category input.

    Meta:
    - model: The associated model for the form.
    - fields: The fields to include in the form.
    """
    CATEGORIES = [
        'Groceries',
        'Utilities',
        'Healthcare',
        'Entertainment',
        'Other',
    ]
    EMPTY_CHOICE = ('', '---------')

    name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Your name'})
    )
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True
    )
    category = forms.ChoiceField(
        choices=[EMPTY_CHOICE] + [(category, category) for category in CATEGORIES],
        required=True
    )
    notes = forms.CharField(
        required=False,
        label='',
        widget=forms.Textarea(attrs={'placeholder': 'Optional: Add any additional notes.', 'rows': 5})
    )

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        return name.capitalize()

    def clean_category(self):
        category = self.cleaned_data.get('category', '')
        return category.capitalize()

    class Meta:
        model = Expense
        fields = ['name', 'amount', 'category', 'notes']

class RegisterForm(UserCreationForm):
    """
    A form for user registration, extending the built-in UserCreationForm.

    Fields:
    - email: The email address of the user.

    Meta:
    - model: The associated model for the form.
    - fields: The fields to include in the form.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class UserProfileForm(forms.ModelForm):
    """
    A form for updating user profile information.

    Fields:
    - date_of_birth: The date of birth of the user (selectable from a date picker).
    - bio: A text field for the user's biography (optional).

    Meta:
    - model: The associated model for the form.
    - fields: The fields to include in the form.
    """
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    bio = forms.CharField(
        required=False,
        label='',
        widget=forms.Textarea(attrs={'placeholder': 'Enter a short bio...', 'rows': 5})
    )

    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'date_of_birth', 'bio']

class CustomPasswordChangeForm(BasePasswordChangeForm):
    """
    A custom form for changing the user's password, extending the built-in PasswordChangeForm.

    Fields:
    - new_password1: The new password input.
    - new_password2: Confirmation of the new password input.

    Meta:
    - model: The associated model for the form (User).
    """
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text="Enter your new password.",
    )

    new_password2 = forms.CharField(
        label="Confirm new password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize form fields if needed

    class Meta:
        model = User  # Replace with your User model if different
