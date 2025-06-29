from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages
from .forms import RegistrationForm
from .models import Client
# Create your views here.
def home(request):
    
    #Grab all the client records from the database
    clients = Client.objects.all()


    #check the logged in user
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
       
        #authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, "You are logged in")
            #then we have to redirect to a page
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('home')
    
    else: 

        return render(request, 'home.html', {'clients': clients})

#this function will be used if we want to use any seperate login page   
# def login_view(request):
#     pass

def logout_view(request):
    # pass
    logout(request)
    messages.success(request, "You are now logged out");
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            #Authenticate and login the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You are registered successfully and welcome to our site")
            return redirect('home')
    else: #incase of registering a user without providing any data in the form
        form = RegistrationForm()
    return render(request, 'register.html', {'form' : form})