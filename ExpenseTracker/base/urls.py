from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.LogOut, name='logout'),
    path('signup/', views.SignUp, name='signup'),
    path('addExpense/', views.AddExpense, name='addexpense'),
    path('writeexcel/', views.WriteEx, name='writeex'),
    path('editExpense/<int:pk>', views.EditExpense, name='editExp'),
    path('deleteExpense/<int:pk>', views.DeleteExp, name='deleteExp'),
]
