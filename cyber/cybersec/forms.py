from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import Device, User
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime

class createUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, label=('First name'))
    last_name =  forms.CharField(max_length=100, required=True, label=('Lanst name'))
    
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2"]
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(("This email is already taken."))
        return email

class UpdateUserForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    phone_number = PhoneNumberField()
    # img_profile = forms.ImageField(required=False)
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['address'].initial = user.address
            self.fields['phone_number'].initial = user.phone_number

    def save(self, user):
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.address = self.cleaned_data.get('address')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.save()
        
class Deive_form(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['user','device_name','ip_address','device_type','operating_system','port_info','auth_credintials','scan_preferces','scan_schudule']
    