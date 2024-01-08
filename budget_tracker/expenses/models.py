from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Users(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='')
    email = models.EmailField(default='', blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=True)

    def __str__(self):
        return self.user.username

class Expense(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=200, null=True)
    notes = models.TextField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} - {self.amount} - {self.category}"

