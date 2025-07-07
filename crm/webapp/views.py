from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages
from .forms import RegistrationForm, AddClientForm, ProductForm
from .models import Client
import csv
from django.http import HttpResponse
from django.db.models import Q
from django.template.loader import get_template
from xhtml2pdf import pisa

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
    
# for product related views
def product(request, client_pk):
    if request.user.is_authenticated:
        client = get_object_or_404(Client, id=client_pk)
        products = client.product.all()
        return render(request, 'product.html', {'client': client,'products': products})
    else:
        messages.success(request, "You need to login to view products")
        return redirect('home')
    
# for adding new product
def new_product(request, client_pk):
    if request.user.is_authenticated:
        client = get_object_or_404(Client, id=client_pk)
        products = client.product.all()
        if request.method == 'POST':
            form = ProductForm(request.POST, client=client)
            if form.is_valid():
                product = form.save(commit=False)
                product.client = client
                product.save()
                messages.success(request, "New product added successfully")
                return render(request, 'product.html', {'client': client, 'products': products})
            else:
                messages.success(request, "Error adding product")
                form = new_product(client=client)
        else:
            form = ProductForm(client=client)
        return render(request, 'new_product.html', {'form': form})
    else:
        messages.success(request, "You need to login to add a new product")
        return redirect('home')

# for searching clients
def search_client(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Client.objects.filter(Q(full_name__icontains=query) | Q(city__icontains=query))
    
    return render(request, 'search_client.html', {'results': results, 'query': query})
    
            
# for deleting a product
from .models import Product

def delete_product(request, product_pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=product_pk)
        client_id = product.client.id
        product.delete()
        messages.success(request, "Product deleted successfully")
        return redirect('product', client_pk=client_id)
    else:
        messages.error(request, "You need to login to delete a product")
        return redirect('home')

# for exporting client data as CSV
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response["Content_Disposition"] = 'attachment, filename="clients.csv'

    #create a csv writer object
    writer = csv.writer(response)

    #write the header row
    writer.writerow([ 'full_name', 'email', 'phone', 'city'])

    #fetch client data from the database
    client_data = Client.objects.all()
    for client in client_data:
        writer.writerow([client.full_name, client.email, client.phone, client.city])
    return response

# for exporting client data as PDF
def export_pdf(request):
    if request.user.is_authenticated:
        clients = Client.objects.all()
        template_path = 'clients_pdf.html'
        context = {'clients': clients}
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="clients.pdf"'
        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    else:
        messages.error(request, "Login to export as PDF")
        return redirect('home')