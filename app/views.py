from django.shortcuts import render
from app.models import Category, Sub_category
# Create your views here.

def Master(request):
    return render(request,'master.html')

def Index(request):
    category = Category.objects.all()
    
    context = {
        'category': category,
    }
    return render(request,'index.html', context)