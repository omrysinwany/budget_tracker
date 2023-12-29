from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/add-expense/', views.add_expense, name='add_expense'),
    path('personal/', views.user_input_name, name='user_input_name'),
    path('personal/<str:name>/', views.expense_detail, name='expense_detail')
]
