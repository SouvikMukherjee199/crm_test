from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

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