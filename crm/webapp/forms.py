from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Client

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True , label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Email'}))
    first_name = forms.CharField(max_length=30,label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ('username',  'first_name', 'last_name', 'password1', 'password2')
        def __init__(self, *args, **kwargs):

            super(RegistrationForm, self).__init__(*args, **kwargs)
         
            self.fields['username'].widget.attrs['class'] = 'form-control'
            self.fields['username'].widget.attrs['placeholder'] = 'Username'

            self.fields['password1'].widget.attrs['class'] = 'form-control'
            self.fields['password1'].widget.attrs['placeholder'] = 'Password'

            self.fields['password2'].widget.attrs['class'] = 'form-control'
            self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'

#Create a form for adding a new client
class AddClientForm(forms.ModelForm):
    full_name = forms.CharField(max_length=30,label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'full_name'}))
    email = forms.EmailField(required=True , label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'email'}))
    phone = forms.CharField(max_length=30,label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'phone'}))
    address = forms.CharField(max_length=30,label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'address'}))
    city = forms.CharField(max_length=30,label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'city'}))
    state =forms.CharField(max_length=30,label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'state'}))
    zip_code = forms.CharField(max_length=30,label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'zip_code'}))
    
    class Meta:
        model = Client
        exclude = ("user",)