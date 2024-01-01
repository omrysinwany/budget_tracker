from datetime import date
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Expense

class UserInput(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(UserInput, self).__init__(*args, **kwargs)
        unique_names_set = set(Expense.objects.filter(user__user=user).values_list('name', flat=True).distinct())
        self.fields['name'] = forms.ChoiceField(choices=[(name, name) for name in unique_names_set])

class NewExpenseForm(forms.Form):
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

    # If you need to use Meta, it should be an inner class
    class Meta:
        model = Expense
        fields = ['name', 'amount', 'category', 'notes']

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"	]