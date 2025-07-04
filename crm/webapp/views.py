from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages
from .forms import RegistrationForm, AddClientForm
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

def client(request, pk):
    if request.user.is_authenticated:
        # Look up the specific client by primary key (pk)
        client_record = Client.objects.get(id=pk)
        return render(request, "client.html", {'client_record': client_record})
    else:
        messages.success(request, "Login to view the client details") 
        return redirect('home')
    
def client_delete(request, pk):
    # Only allow deletion if the user is authenticated
    if request.user.is_authenticated: 
        # Look up the specific client by primary key (pk)
        delete_record = Client.objects.get(id=pk)
        delete_record.delete()
        messages.success(request, "Client record deleted successfully")
        return redirect('home')
    else:
        messages.success(request, "Login to delete the client record") 
        return redirect('home')
    
def add_client(request):
    form = AddClientForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_client = form.save()
                messages.success(request, "New client added successfully") 
                return redirect('home')
        return render(request, 'add_client.html', {'form': form})
    else: 
        messages.success(request, "Login to add a new client") 
        
        return redirect('home')
    
    #For updating the client record

def client_update(request, pk):
    if request.user.is_authenticated:
        # Look up the specific client by primary key (pk)or id
        client_record = Client.objects.get(id=pk)
        form = AddClientForm(request.POST or None, instance=client_record)
        if request.method == 'POST':
            if form.is_valid:
                update_client = form.save()
                messages.success(request, "Client record updated successfully")
                return redirect('home')
        else:
            form = AddClientForm(instance=client_record)
        return render(request, 'client_update.html', {'form': form})
    else:
        messages.success(request, "Login to update the client record") 
        return redirect('home')