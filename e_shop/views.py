from django.db import transaction

from django.shortcuts import render, redirect, HttpResponse
from app.models import Category, Product, UserCreateForm, Contact_us, Order, Brand, Review, FAQ, About
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.contrib.auth.models import User
import razorpay
from django.conf import settings
from django.contrib import messages

# Create your views here.

def Master(request):
    return render(request, 'master.html')

def Index(request):
    category = Category.objects.all()
    product = Product.objects.all()
    categoryID = request.GET.get('category')
    
    brand = Brand.objects.all()
    brandID = request.GET.get('brand')
         
    if categoryID:
        product = Product.objects.filter(sub_category=categoryID).order_by('-id')
        
    elif brandID:
        product = Product.objects.filter(brand=brandID).order_by('-id')

    else:
        product = Product.objects.all()
    
    context = {
        'category': category,
        'product': product,
        'brand': brand,
    }
    
    about_email = request.POST.get('about')
    if about_email:
        about = About(email=about_email)
        about.save()
        
    return render(request, 'index.html', context)


def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            if User.objects.filter(username=username).exists():
                # Username already exists
                form.add_error('username', 'Username already exists. Please choose a different username.')
                return render(request, 'registration/signup.html', {'form': form})
            if User.objects.filter(email=email).exists():
                # Email already exists
                form.add_error('email', 'Email already registered. Please use a different email address.')
                return render(request, 'registration/signup.html', {'form': form})
            
            # Continue with signup process if no duplicate username or email
            new_user = form.save()
            new_user = authenticate(
                username=username,
                password=form.cleaned_data['password1'],
            )
            login(request, new_user)
            return redirect('index')
    else:
        form = UserCreateForm()

    context = {
        'form': form,
    }

    # Check if user is already authenticated
    if request.user.is_authenticated:
        return redirect('index')  # Redirect to index if user is already authenticated

    # Attempt to retrieve user ID from session
    user_id = request.session.get('user_id')
    if user_id:
        user = authenticate(request, user_id=user_id)
        if user is not None:
            login(request, user)
            return redirect('index')

    return render(request, 'registration/signup.html', context)


@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    
    # Check if the product is in the cart
    if str(product.id) in cart.cart:
        cart.cart[str(product.id)]['quantity'] -= 1
        if cart.cart[str(product.id)]['quantity'] == 0:
            del cart.cart[str(product.id)]
        cart.save()

    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    with transaction.atomic():    
        about_email = request.POST.get('about')
        if about_email:
            about = About(email=about_email)
            about.save()
            
    return render(request, 'cart/cart_detail.html')

def Contact_page(request):
    if request.method == 'POST':
        with transaction.atomic():
            contact = Contact_us(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                subject=request.POST.get('subject'),
                message=request.POST.get('message'),
            )
            contact.save()
            # Assuming you have a field named 'about' in your form
            about_email = request.POST.get('about')
            if about_email:
                about = About(email=about_email)
                about.save()
    
    return render(request, 'contact.html')


def Checkout(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        pincode = request.POST.get('pincode')
        cart = request.session.get('cart')
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(pk=uid)
                
        with transaction.atomic():
            for i in cart:
                a = int(cart[i]['price'])
                b = cart[i]['quantity']
                total = a * b
                order = Order(
                    user=user,
                    product=cart[i]['name'],
                    price=cart[i]['price'],
                    quantity=cart[i]['quantity'],
                    image=cart[i]['image'],
                    address=address,
                    phone=phone,
                    pincode=pincode,
                    total=total,
                )
                order.save()
            
            about_email = request.POST.get('about')
            if about_email:
                about = About(email=about_email)
                about.save()
    
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        # Calculate the total order amount
        order_amount = sum(int(item['price']) * int(item['quantity']) for item in cart.values()) * 100  # Convert to paise

        if order_amount < 1:
            return redirect('error')
        # Create a Razorpay order
        order_currency = 'INR'
        order_receipt = 'order_rcptid_11'  # You may want to generate a unique receipt ID
        response = client.order.create({'amount': order_amount, 'currency': order_currency, 'receipt': order_receipt, 'payment_capture': '1'})

        # Clear the cart after creating the order
        if response.get('status') == 'created':
            request.session['cart'] = {}
        # Redirect the user to the Razorpay checkout page
        return render(request, 'checkout.html', {'order_id': response['id'], 'amount': order_amount, 'currency': order_currency})
        
    return HttpResponse("This is a checkout page !!")


def Your_Order(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)
    
    with transaction.atomic():
        order = Order.objects.filter(user=user)
    
        about_email = request.POST.get('about')
        if about_email:
            about = About(email=about_email)
            about.save()
    
        context = {
            'order': order
        }
    return render(request, 'order.html', context)

def Product_page(request):
    category = Category.objects.all()
    categoryID = request.GET.get('category')
    brand = Brand.objects.all()
    brandID = request.GET.get('brand')
         
    if categoryID:
        product = Product.objects.filter(sub_category=categoryID).order_by('-id')
        
    elif brandID:
        product = Product.objects.filter(brand=brandID).order_by('-id')

    else:
        product = Product.objects.all()
        
    about_email = request.POST.get('about')
    if about_email:
        about = About(email=about_email)
        about.save()
        
    context = {
        'category': category,
        'brand': brand,
        'product': product,
    }
    return render(request, 'product.html',  context)


def Product_detail(request, id):
    category = Category.objects.all()
    product = Product.objects.all()
    categoryID = request.GET.get('category')
    
    brand = Brand.objects.all()
    brandID = request.GET.get('brand')
         
    if categoryID:
        product = Product.objects.filter(sub_category=categoryID).order_by('-id')
        
    elif brandID:
        product = Product.objects.filter(brand=brandID).order_by('-id')

    else:
        product = Product.objects.all()
        
    product = Product.objects.filter(id=id).first()
    
    context = {
        'product': product,
        'category': category,
        'product': product,
        'brand': brand,
    }
    
    if request.method == 'POST':
        with transaction.atomic():
            review = Review(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                comment=request.POST.get('comment'),
            )
            review.save()

            about_email = request.POST.get('about')
            if about_email:
                about = About(email=about_email)
                about.save()
    
    return render(request, 'product_detail.html', context)

def Search(request):
    query = request.GET['query']
    product = Product.objects.filter(name__icontains=query)
    context = {
        'product': product,
    }
    
    return render(request, 'search.html', context)

def faq_list(request):
    with transaction.atomic():
        faqs = FAQ.objects.all()
    
        about_email = request.POST.get('about')
        if about_email:
            about = About(email=about_email)
            about.save()
    
    return render(request, 'faq.html', {'faqs': faqs})

def error(request):
    return render(request, 'error.html')

def Policy(request):
    return render(request, 'policy.html')

def Info(request):
    return render(request, 'info.html')
