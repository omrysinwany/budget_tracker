import os
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import *
from .forms import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from django.conf import settings

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

def modify_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)

    if request.method == 'POST':
        form = NewExpenseForm(request.POST)
        if form.is_valid():
            # Update the expense object with the form data
            expense.name = form.cleaned_data['name']
            expense.amount = form.cleaned_data['amount']
            expense.category = form.cleaned_data['category']
            expense.notes = form.cleaned_data['notes']
            expense.save()
            return redirect('expense_list')
    else:
        # Populate the form with existing expense data
        form = NewExpenseForm(initial={
            'name': expense.name,
            'amount': expense.amount,
            'category': expense.category,
            'notes': expense.notes,
            'date': expense.date,
        })

    return render(request, 'modify_expense.html', {'form': form, 'expense': expense})

def delete_expense(request, expense_id):
    # Get the expense object or return a 404 response if not found
    expense = get_object_or_404(Expense, id=expense_id)

    # Delete the expense
    expense.delete()

    # Redirect to the expense list page or any other desired page
    return redirect('expense_list')

@login_required(login_url="/login")
def add_expense(request):

    users_instance = Users.objects.get(user=request.user)

    if request.method == "POST":
        form = NewExpenseForm(request.POST)

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
        form = NewExpenseForm()

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

@login_required(login_url="/login")
def statistics_view(request):
    print("Entering user_statistics_view function")
    
    # Fetch user-specific expenses
    user_expenses = Expense.objects.filter(user__user=request.user)
    
    # Create a DataFrame from the expenses
    df = pd.DataFrame(list(user_expenses.values()))
    print("DataFrame created successfully")
    print("DataFrame columns:", df.columns)  # Print the columns of the DataFrame

    # Add some debug prints to check the structure of df
    print("DataFrame shape:", df.shape)
    print("DataFrame head:", df.head())
    
    # Calculate statistics
    total_expenses = df['amount'].sum()
    average_expense = df['amount'].mean()
    category_counts = df['category'].value_counts()

    # Define the directory for saving images
    images_dir = os.path.join(settings.BASE_DIR, 'expenses', 'static', 'images')
    
    # Ensure the directory exists, create it if not
    os.makedirs(images_dir, exist_ok=True)

    # Switch backend to 'Agg' to avoid main thread issues
    plt.switch_backend('Agg')

    # Plot a bar chart of expenses by category
    plt.bar(category_counts.index, category_counts.values)
    plt.title('Expense Distribution by Category')
    plt.xlabel('Category')
    plt.ylabel('Number of Expenses')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save the plot as an image
    category_counts_plot = 'category_counts_plot.png'
    plt.savefig(os.path.join(images_dir, category_counts_plot))
    plt.close()

    # Prepare context for rendering the template
    context = {
        'total_expenses': total_expenses,
        'average_expense': average_expense,
        'category_counts_plot': category_counts_plot,
    }

    # Render the template with the context
    return context

@login_required(login_url="/login")
def user_statistics_view(request):
    print("Entering user_statistics_view function")

    # Fetch user-specific expenses
    user_expenses = Expense.objects.filter(user__user=request.user)

    # Create a DataFrame from the expenses
    df = pd.DataFrame(list(user_expenses.values()))
    print("DataFrame created successfully")
    print("DataFrame columns:", df.columns)  # Print the columns of the DataFrame

    # Add some debug prints to check the structure of df
    print("DataFrame shape:", df.shape)
    print("DataFrame head:", df.head())

    # Calculate statistics
    total_expenses = df['amount'].sum()
    average_expense = df['amount'].mean()
    category_counts = df['category'].value_counts()

     # Define the directory for saving images
    images_dir = os.path.join(settings.BASE_DIR, 'expenses', 'static', 'images')
    
    # Ensure the directory exists, create it if not
    os.makedirs(images_dir, exist_ok=True)

    # Switch backend to 'Agg' to avoid main thread issues
    plt.switch_backend('Agg')

    # Create a pie chart of expenses by category
    plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title('Expense Distribution by Category')

     # Save the plot as an image
    category_distribution_plot = 'category_distribution_plot.png'
    plt.savefig(os.path.join(images_dir, category_distribution_plot))
    plt.close()

    # Prepare context for rendering the template
    context = {
        'total_expenses': total_expenses,
        'average_expense': average_expense,
        'category_distribution_plot': category_distribution_plot,
    }

    # Render the template with the context
    return context

@login_required(login_url="/login")
def combined_statistics(request):
     # Call each statistics function and get the context dictionaries
    bar_chart_context = statistics_view(request)
    pie_chart_context = user_statistics_view(request)

    # Combine the context dictionaries
    combined_context = {
        'category_counts_plot': bar_chart_context['category_counts_plot'],
        'category_distribution_plot': pie_chart_context['category_distribution_plot'],
        'total_expenses': bar_chart_context['total_expenses'],
    }

    # Render a template with the combined context
    return render(request, 'statistic.html', combined_context)



