from django.shortcuts import redirect, render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Category, Expense
from .forms import *
import numpy as np
import pandas as pd

def home(request):
    return render(request, "home.html")


def expense_list(request):
    expenses = Expense.objects.all()
    return render(request, 'expense_list.html', {'expenses': expenses})

def add_expense(request):
    if request.method == "POST":
        form = NewExpense(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            amount = form.cleaned_data["amount"]
            date = form.cleaned_data["date"]
            Category = form.cleaned_data["Category"]
            notes = form.cleaned_data["notes"]
            new_expense = Expense(name=name, amount=amount, date=date, notes=notes, Category=Category)
            new_expense.save()

            return redirect('add_expense')

    else:
        form = NewExpense()

    return render(request, 'add_expense.html', {'form': form})

def expense_detail(request, name):
    related_expenses = Expense.objects.filter(name=name)
    return render(request, 'expense_detail.html', {'related_expenses': related_expenses})

def user_input_name(response):
    if response.method == "POST":
        form = UserInput(response.POST)

        if form.is_valid():
            expense_instance = form.cleaned_data["name"]
            url = reverse('expense_detail', args=[expense_instance])

        return HttpResponseRedirect(url)
    else: 
        form = UserInput()
    return render(response, 'input_name.html', {'form': form})


def expense_statistics(request):
    expenses = Expense.objects.all()
    data = {
        'Amount': [expense.amount for expense in expenses],
        'Category': [expense.Category.name for expense in expenses],
    }
    df = pd.DataFrame(data)
    statistics = {
        'Total': df['Amount'].sum(),
        'Average': df['Amount'].mean(),
        'Category_Count': df['Category'].value_counts().to_dict(),
    }
    return render(request, 'expenses/expense_statistics.html', {'statistics': statistics})
