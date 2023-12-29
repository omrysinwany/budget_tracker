from django import forms
from .models import Category, Expense

class UserInput(forms.Form):
    unique_names_set = set(Expense.objects.values_list('name', flat=True).distinct())
    name = forms.ChoiceField(choices=[(name, name) for name in unique_names_set])

class NewExpense(forms.Form):
    name = forms.CharField(max_length=200,required=True, widget=forms.TextInput(attrs={'placeholder': 'Your name'}))
    amount = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
    Category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)
    date = forms.DateField(required=False, help_text="Optional", widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    notes = forms.CharField(required=False, label='', widget=forms.Textarea(attrs={'placeholder': 'Optional: Add any additional notes.', 'rows': 5}))
    

    