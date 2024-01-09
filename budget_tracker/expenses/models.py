# models.py

from django.db import models
from django.contrib.auth.models import User

class Users(models.Model):
    """
    Represents the relationship between a User model and additional user-related information.

    Fields:
    - user: A foreign key relationship with the built-in User model in Django.

    Methods:
    - __str__: Returns a string representation of the user's username.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class UserProfile(models.Model):
    """
    Represents additional profile information for a user.

    Fields:
    - user: A one-to-one relationship with the built-in User model in Django.
    - name: The name of the user (default is an empty string).
    - email: The email address of the user (default is an empty string, can be blank).
    - date_of_birth: The date of birth of the user (nullable and blank).
    - bio: A text field for the user's biography (blank).
    - budget: The budget associated with the user (default is 0.0, nullable).

    Methods:
    - __str__: Returns a string representation of the user's username.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='')
    email = models.EmailField(default='', blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=True)

    def __str__(self):
        return self.user.username

class Expense(models.Model):
    """
    Represents an expense associated with a specific user.

    Fields:
    - user: A foreign key relationship with the Users model.
    - amount: The amount of the expense.
    - date: The date when the expense occurred.
    - category: The category of the expense (nullable).
    - notes: Additional notes related to the expense.
    - name: The name or description of the expense.

    Methods:
    - __str__: Returns a formatted string representation of the expense.
    """
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=200, null=True)
    notes = models.TextField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} - {self.amount} - {self.category}"
