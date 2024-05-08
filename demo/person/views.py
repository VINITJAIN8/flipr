from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Intro,ExpenseCategory

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Intro.objects.create(user=user_model)
                new_profile.save()
                return HttpResponse('hellow')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        
    else:
        return render(request, 'signup.html')
    

def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            # return render(request,'profile.html')
            return HttpResponse('heelo')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html')
    

@login_required(login_url='signin')
def additemname(request):
    if request.method=='POST':
        name=request.POST['itemname']
        new=ExpenseCategory(itemname=name)
        new.save()

        return HttpResponse('done')
    return render(request,'create.html')

@login_required(login_url='signin')
def listitem(request):
    lis=ExpenseCategory.objects.all()
    return render(request,'list.html',{'lis':lis})


@login_required(login_url='signin')
def delete(request,id):
    d=ExpenseCategory.objects.filter(id=id)
    d.delete()
    return HttpResponse('delete')


@login_required(login_url='signin')
def update(request, id):
    if request.method == 'POST':
        expense_category = ExpenseCategory.objects.get(id=id)
        expense_category.itemname = request.POST['itemname']
        
        expense_category.save()
        return HttpResponse('success')
    else:
        return render(request, 'update.html')

# Create your views here.