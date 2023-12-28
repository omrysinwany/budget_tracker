from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/<int:expense_id>/', views.expense_detail, name='expense_detail'),
]
