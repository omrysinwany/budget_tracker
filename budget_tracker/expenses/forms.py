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

class NewExpense(forms.Form):
    CATEGORIES = [
        'Groceries',
        'Utilities',
        'Healthcare',
        'Entertainment',
        'Other',
    ]
    EMPTY_CHOICE = ('', '---------')

    Name = forms.CharField(max_length=200,required=True, widget=forms.TextInput(attrs={'placeholder': 'Your name'}))
    Amount = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
    Category = forms.ChoiceField(choices=[EMPTY_CHOICE] + [(category, category) for category in CATEGORIES], required=True)
    Notes = forms.CharField(required=False, label='', widget=forms.Textarea(attrs={'placeholder': 'Optional: Add any additional notes.', 'rows': 5}))

    def clean_Name(self):
        name = self.cleaned_data.get('Name', '')
        return name.capitalize()

    def clean_Category(self):
        category = self.cleaned_data.get('Category', '')
        return category.capitalize()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"	]