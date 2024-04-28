from django.contrib import admin
from .models import Category, Sub_category, Product, Contact_us, Order, Brand, Review, FAQ, About
# Register your models here.

admin.site.register(Category)
admin.site.register(Sub_category)
admin.site.register(Product)
admin.site.register(Contact_us)
admin.site.register(Order)
admin.site.register(Brand)
admin.site.register(Review)
admin.site.register(FAQ)
admin.site.register(About)