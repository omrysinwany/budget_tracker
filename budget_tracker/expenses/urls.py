from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("sign-up/", views.sign_up, name="sign_up"),
    path('expenses/', views.expense_list, name='expense_list'),
    path('modify_expense/<int:expense_id>/', views.modify_expense, name='modify_expense'),
    path('delete_expense/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('expenses/add-expense/', views.add_expense, name='add_expense'),
    path('personal/', views.user_input_name, name='user_input_name'),
    path('personal/<str:name>/', views.expense_detail, name='expense_detail'),
    path('statistics/', views.combined_statistics, name='combined_statistics'),
    
]
