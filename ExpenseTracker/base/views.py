from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Expense
import datetime
import pandas as pd
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.


@login_required
def index(request):
    if request.GET.get('month', None):
        month = request.GET['month']
        if month == 'aggregate':
            expenses = request.user.expenses.all().order_by('-Date')
            return render(request, 'index.html',{'expenses': expenses})
        year, month = month.split('-')
        print(month, year)

    else:
        day = datetime.date.today()
        month, year = day.month, day.year
    expenses = request.user.expenses.filter(Date__month = month, Date__year = year).order_by('-Date')
    return render(request, 'index.html',{'expenses': expenses, 'month':month, 'year':year})

def loginView(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')

        else:
            messages.add_message(request, messages.WARNING, "Invalid Credentials")

    return render(request, 'login.html')

def LogOut(request):
    logout(request)
    return redirect('index')

def SignUp(request):
    if request.method == 'POST':

        username = request.POST['username']
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.WARNING, "Username exists")
        elif User.objects.filter(email=email).exists():
            messages.add_message(request, messages.WARNING, "Account with same email id exists")
        elif password1!=password2:
            messages.add_message(request, messages.WARNING, "Passwords don't match")
        else:
            user = User.objects.create_user(username=username,first_name=firstname, last_name=lastname, email=email, password=password1)
            user.save()
            messages.add_message(request, messages.SUCCESS, "New User Created")
            return redirect('index')
        # print(username)
    return render(request, 'signup.html')


@login_required
def AddExpense(request):
    if request.method == 'POST':
        user = request.user
        expense = float(request.POST['expense'])
        description = request.POST['description']
        date = request.POST['date']
        item = Expense(user=user, expense=expense, description=description, Date=date)
        item.save()
        return redirect('index')

    return render(request,'add_expense.html')

@login_required
def EditExpense(request, pk):
    expense = Expense.objects.get(pk=pk)
    # print(expense.Date.month, expense.Date.year, expense.Date.day)
    month = str(expense.Date.month)
    day = str(expense.Date.day)
    if len(month)==1:
        month = '0' + month 
    if len(day) == 1:
        day = '0' + day
    date = {
        'month': month,
        'day' : day
    }
    if expense.user != request.user:
        return redirect('index')
    if request.method == 'POST':
        expense.expense = request.POST['expense']
        expense.description = request.POST['description']
        expense.Date = request.POST['date']
        expense.save()
        return redirect('index')

    return render(request, 'edit_expense.html', {'expense': expense, 'day': date})

def DeleteExp(request, pk):
    expense = Expense.objects.get(pk=pk)
    # print(expense.Date.month, expense.Date.year, expense.Date.day)
    if expense.user != request.user:
        return redirect('index')
    expense.delete()
    return redirect('index')




@api_view(['GET'])
def WriteEx(request):
    user = User.objects.filter(username=request.GET['user']).first()
    month = request.GET['month']
    print(user.username)
    print(month)
    if month!='aggregate':
        year = request.GET['year']
        expenses = user.expenses.filter(Date__month = month, Date__year = year).order_by('-Date')
    else:
        expenses = user.expenses.all().order_by('-Date')

    print(expenses)

    df = []
    i = 1
    total = 0
    for item in expenses:
        expense = {}
        expense['SI No.'] = i
        expense['Date'] = str(item.Date)
        expense['Description'] = item.description
        expense['Expense (in Rs)'] = float(item.expense)
        total += float(item.expense)
        df.append(expense)
        i+=1
    expense = {}
    expense['SI No.'] = 'Total'
    expense['Date'] = ''
    expense['Description'] = ''
    expense['Expense (in Rs)'] = total
    df.append(expense)

    df = pd.DataFrame(df)
    df = df.set_index('SI No.')
    df.to_excel(f'static/excel/Expenses_{user.username}.xls')




    # else:
    #     return Response({'message':'Invalid Request'})

    return Response({'message':'success'})