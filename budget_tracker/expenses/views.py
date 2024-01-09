import os
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login, logout, authenticate
from .models import *
from .forms import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.conf import settings

def home(request):
    return render(request, "home.html")

def no_expenses(request):
    return render(request, "no_expenses.html")

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            UserProfile.objects.create(user=user)

            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})

@login_required(login_url="/login")
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form})

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')

def reset_password(request):
    return CustomPasswordResetView.as_view()(request)

@login_required(login_url="/login")
def user_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            # Update the UserProfile object with the form data
            user_profile = form.save()

            # Update the budget field if provided in the form
            budget = form.cleaned_data.get('budget')
            if budget is not None:
                user_profile.budget = budget
                user_profile.save()

            messages.success(request, 'Your profile has been successfully updated.')
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'user_profile.html', {'form': form, 'user_profile': user_profile})

@login_required(login_url="/login")
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
