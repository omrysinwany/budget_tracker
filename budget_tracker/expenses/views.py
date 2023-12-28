from django.shortcuts import render, HttpResponse
from .models import Expense
import numpy as np
import pandas as pd

def home(request):
    return render(request, "home.html")


def expense_list(request):
    expenses = Expense.objects.all()
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})


def expense_detail(request, expense_id):
    expense = Expense.objects.get(id=expense_id)
    return render(request, 'expenses/expense_detail.html', {'expense': expense})


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
