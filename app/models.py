from typing import Any
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import datetime
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150)
    
    def __str__(self):
        return self.name

class Sub_category(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.name
    
class Product(models.Model):
    Availability = (('In Stock', 'In Stock'), ('Out of Stock', 'Out of Stock'),)
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
    sub_category = models.ForeignKey(Sub_category, on_delete=models.CASCADE, default=None)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='ecommerce/pimg')
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    Availability = models.CharField(choices=Availability, null=True, max_length=100)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email', error_messages={'exists': 'This already exists!'})
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email Address'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'   
    
    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
    ## INBUILT FUNCTION:
    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError(self.fields['email'].error_message['exists!'])
    #     return self.cleaned_data['email']
    
    
    ## USER DEFINED FUNCTION IMPLEMENTED BY ME:
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use. Please use a different email address.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken. Please choose a different username.')
        return username
    
class Contact_us(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    
    def __str__(self) -> str:
        return self.name
    
class Order(models.Model):
    image = models.ImageField(upload_to='ecommerce/order/image')
    product = models.CharField(max_length=1000, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.CharField(max_length=5)
    total = models.CharField(max_length=1000, default='')
    address = models.TextField()
    phone = models.CharField(max_length=10)
    pincode = models.CharField(max_length=10)
    date = models.DateField(default=datetime.datetime.today)
    
    def __str__(self)->str:
        return self.product
    
class Review(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    comment = models.TextField()
    
    def __str__(self):
        return f"{self.id} - {self.name}" 

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    
    def __str__(self) -> str:
        return self.question

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer']
        
class About(models.Model):
    email = models.EmailField(max_length=255, null=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.email}" 
