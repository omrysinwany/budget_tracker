from django.urls import path
from . import views
from .views import reset_password
from django.contrib.auth import views as auth_views
from .views import csrf_failure_view


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
    path('no_expenses/', views.no_expenses, name='no_expenses'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('reset_password/', reset_password, name='reset_password'),
    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('update_budget/', views.update_budget, name='update_budget'),
    path('make_budget/', views.make_budget, name='make_budget'),
    path('csrf_failure/', csrf_failure_view, name='csrf_failure'),
    
    
]
