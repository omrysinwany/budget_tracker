# views.py

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
    """Render the home page."""
    return render(request, "home.html")

def no_expenses(request):
    """Render a page for users with no expenses."""
    return render(request, "no_expenses.html")

def sign_up(request):
    """Handle user registration."""
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
    """Handle password change for logged-in users."""
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form})

class CustomPasswordResetView(PasswordResetView):
    """Customize the password reset view."""
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')

def reset_password(request):
    """Handle password reset request."""
    return CustomPasswordResetView.as_view()(request)

@login_required(login_url="/login")
def user_profile(request):
    """View and update user profile."""
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
    """List the expenses of the logged-in user."""
    try:
        users_instance = Users.objects.get(user=request.user)
        user_profile = get_object_or_404(UserProfile, user=request.user)
        expenses = Expense.objects.filter(user=users_instance)

        if not expenses.exists():
            # If the user has no expenses, redirect to another template
            return render(request, 'no_expenses.html')
    except Users.DoesNotExist:
        # Handle the case where the Users instance does not exist
        return render(request, 'no_expenses.html')

    return render(request, 'expense_list.html', {'expenses': expenses, 'user_profile': user_profile})

def modify_expense(request, expense_id):
    """Modify an existing expense."""
    expense = get_object_or_404(Expense, id=expense_id)

    if request.method == 'POST':
        form = NewExpenseForm(request.POST)
        if form.is_valid():
            # Update the expense object with the form data
            expense.name = form.cleaned_data['name']
            expense.amount = form.cleaned_data['amount']
            expense.category = form.cleaned_data['category']
            expense.notes = form.cleaned_data['notes']
            
            user_profile = UserProfile.objects.get(user=request.user)
            remaining_budget = user_profile.budget - expense.amount

            if remaining_budget < 0 and user_profile.budget != 0:
                print("<0")
                messages.warning(request, 'Failed to add the expense. This expense exceeds the budget.')
            
            elif user_profile.budget == 0:
                print("0")
                messages.success(request, 'Expense has been successfully added..')
                expense.save()
                return redirect('expense_list')

            else:
                print(">0")
                messages.success(request, 'Expense has been successfully added..')
                expense.save()
                # Update the user's remaining budget
                user_profile.budget = remaining_budget
                user_profile.save()
        
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
    """Delete an existing expense."""
    # Get the expense object or return a 404 response if not found
    expense = get_object_or_404(Expense, id=expense_id)

    # Delete the expense
    expense.delete()

    # Redirect to the expense list page or any other desired page
    return redirect('expense_list')

@login_required(login_url="/login")
def add_expense(request):
    """Add a new expense for the logged-in user."""
    users_instance, created = Users.objects.get_or_create(user=request.user)
    users_instance = Users.objects.get(user=request.user)

    if request.method == "POST":
        form = NewExpenseForm(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data

            name = cleaned_data.get("name", "")
            amount = cleaned_data.get("amount", 0)
            category = cleaned_data.get("category", "")
            notes = cleaned_data.get("notes", "")

            # Check if adding the expense exceeds the budget
            user_profile = UserProfile.objects.get(user=request.user)
            remaining_budget = user_profile.budget - amount

            if remaining_budget < 0 and user_profile.budget != 0:
                print("<0")
                messages.warning(request, 'Failed to add the expense. This expense exceeds the budget.')
            
            elif user_profile.budget == 0:
                print("0")
                messages.success(request, 'Expense has been successfully added..')
                new_expense = Expense(name=name, amount=amount, category=category, notes=notes, date=date.today(), user=users_instance)
                new_expense.save()
                return redirect('expense_list')

            else:
                print(">0")
                messages.success(request, 'Expense has been successfully added..')
                new_expense = Expense(name=name, amount=amount, category=category, notes=notes, date=date.today(), user=users_instance)
                new_expense.save()
                # Update the user's remaining budget
                user_profile.budget = remaining_budget
                user_profile.save()
        
            return redirect('expense_list')

    else:
        form = NewExpenseForm()

    return render(request, 'add_expense.html', {'form': form})

@login_required(login_url="/login")
def make_budget(request):
    """Set or update the budget for the logged-in user."""
    if request.method == 'POST':
        new_budget = request.POST.get('budget')
        user_instance = request.user.userprofile  # Adjust accordingly based on your user model
              
        try:
            # Ensure the input is a valid number
            new_budget_float = float(new_budget)
            
            # Update the user's budget
            user_instance.budget = new_budget_float
            user_instance.save()
            
            messages.success(request, 'Budget updated successfully.')
            
        except ValueError:
            messages.error(request, 'Invalid budget value. Please enter a valid number.')

    # Redirect to the add_expense page
    return redirect('add_expense')

@login_required(login_url="/login")
def update_budget(request):
    """Update the budget for the logged-in user."""
    if request.method == 'POST':
        new_budget = request.POST.get('budget')
        user_instance = request.user.userprofile  # Adjust accordingly based on your user model
              
        try:
            # Ensure the input is a valid number
            new_budget_float = float(new_budget)
            
            # Update the user's budget
            user_instance.budget = new_budget_float
            user_instance.save()
            
            messages.success(request, 'Budget updated successfully.')
            
        except ValueError:
            messages.error(request, 'Invalid budget value. Please enter a valid number.')

    return redirect('expense_list')

@login_required(login_url="/login")
def expense_detail(request, name):
    """Display details of expenses with a specific name."""
    related_expenses = Expense.objects.filter(name=name)
    return render(request, 'expense_detail.html', {'related_expenses': related_expenses})

@login_required(login_url="/login")
def user_input_name(request):
    """Handle user input for expense name and redirect to related expenses."""
    url = "/home"  # Set a default URL

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
    """Generate and return context for statistics view."""
    # Fetch user-specific expenses
    user_expenses = Expense.objects.filter(user__user=request.user)
    
    # Create a DataFrame from the expenses
    df = pd.DataFrame(list(user_expenses.values()))

    # Calculate statistics
    total_expenses = df['amount'].sum()
    average_expense = df['amount'].mean()
    name_counts = df['name'].value_counts()

    # Define the directory for saving images
    images_dir = os.path.join(settings.BASE_DIR, 'expenses', 'static')
    
    # Ensure the directory exists, create it if not
    os.makedirs(images_dir, exist_ok=True)

    # Switch backend to 'Agg' to avoid main thread issues
    plt.switch_backend('Agg')

    # Plot a bar chart of expenses by category
    plt.bar(name_counts.index, name_counts.values)
    plt.title('Expense Distribution by Name')
    plt.xlabel('Name')
    plt.ylabel('Number of Expenses')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save the plot as an image
    name_counts_plot = 'name_counts_plot.png'
    plt.savefig(os.path.join(images_dir, name_counts_plot))
    plt.close()

    # Prepare context for rendering the template
    context = {
        'total_expenses': total_expenses,
        'average_expense': average_expense,
        'name_counts_plot': name_counts_plot,
    }

    return context

@login_required(login_url="/login")
def user_statistics_view(request):
    """Generate and return context for user-specific statistics view."""
    # Fetch user-specific expenses
    user_expenses = Expense.objects.filter(user__user=request.user)

    # Create a DataFrame from the expenses
    df = pd.DataFrame(list(user_expenses.values()))

    # Calculate statistics
    total_expenses = df['amount'].sum()
    average_expense = df['amount'].mean()
    category_counts = df['category'].value_counts()

     # Define the directory for saving images
    images_dir = os.path.join(settings.BASE_DIR, 'expenses', 'static')
    
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

    return context

@login_required(login_url="/login")
def combined_statistics(request):
    """Combine multiple statistics and render the statistics template."""
    try:
        users_instance = Users.objects.get(user=request.user)
        expenses = Expense.objects.filter(user=users_instance)
        user_profile = get_object_or_404(UserProfile, user=request.user)

        if not expenses.exists():
            # If the user has no expenses, redirect to another template
            return render(request, 'no_expenses.html')
    except Users.DoesNotExist:
        # Handle the case where the Users instance does not exist
        return render(request, 'no_expenses.html')

     # Call each statistics function and get the context dictionaries
    bar_chart_context = statistics_view(request)
    pie_chart_context = user_statistics_view(request)

    # Combine the context dictionaries
    combined_context = {
        'name_counts_plot': bar_chart_context['name_counts_plot'],
        'category_distribution_plot': pie_chart_context['category_distribution_plot'],
        'total_expenses': bar_chart_context['total_expenses'],
        'user_profile': user_profile,
    }

    # Render a template with the combined context
    return render(request, 'statistic.html', combined_context)

def csrf_failure_view(request, reason=""):
    """
    Custom view for handling CSRF failures.
    You can customize this function based on your requirements.
    """
    context = {'reason': reason}
    return render(request, 'csrf_failure.html', context)
