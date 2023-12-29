from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    notes = models.TextField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

