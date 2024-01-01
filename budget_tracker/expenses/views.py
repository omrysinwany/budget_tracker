from django.shortcuts import redirect, render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import *
from .forms import *
import numpy as np
import pandas as pd

@login_required(login_url="/login")
def home(request):
    return render(request, "home.html")

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})


@login_required(login_url="/login")
def expense_list(request):

    users_instance = Users.objects.get(user=request.user)
    expenses = Expense.objects.filter(user=users_instance)
    return render(request, 'expense_list.html', {'expenses': expenses})

@login_required(login_url="/login")
def add_expense(request):

    users_instance = Users.objects.get(user=request.user)

    if request.method == "POST":
        form = NewExpense(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            
            name = cleaned_data.get("Name", "")
            amount = cleaned_data.get("Amount", 0)
            category = cleaned_data.get("Category", "")
            notes = cleaned_data.get("Notes", "")

            new_expense = Expense(name=name, amount=amount, category=category, notes=notes,date=date.today(), user=users_instance)
            new_expense.save()

            return redirect('expense_list')

    else:
        form = NewExpense()

    return render(request, 'add_expense.html', {'form': form})

@login_required(login_url="/login")
def expense_detail(request, name):
    related_expenses = Expense.objects.filter(name=name)
    return render(request, 'expense_detail.html', {'related_expenses': related_expenses})

@login_required(login_url="/login")
def user_input_name(request):
    if request.method == "POST":
        current_user = request.user
        form = UserInput(user=current_user, data=request.POST)

        if form.is_valid():
            expense_instance = form.cleaned_data["name"]
            url = reverse('expense_detail', args=[expense_instance])

        return HttpResponseRedirect(url)
    else: 
        form = UserInput(user=request.user)
    return render(request, 'input_name.html', {'form': form})


def expense_statistics(request):
    expenses = Expense.objects.all()
    data = {
        'Amount': [expense.amount for expense in expenses],
        'Category': [expense.name for expense in expenses],
    }
    df = pd.DataFrame(data)
    statistics = {
        'Total': df['Amount'].sum(),
        'Average': df['Amount'].mean(),
        'Category_Count': df['Category'].value_counts().to_dict(),
    }
    return render(request, 'expenses/expense_statistics.html', {'statistics': statistics})
