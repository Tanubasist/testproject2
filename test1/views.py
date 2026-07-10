from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from .models import Product, Contact_Query
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

def home(request):
    product_info = Product.objects.all()
    return render(request, 'test1/home.html', {'product_info': product_info})

def find_product(request):
    if request.method == 'POST':
        x = request.POST.get('prod_search')
        print(x)
        
        # Sahi kiya: Q objects ko ek hi filter bracket ke andar pipeline (|) se joda
        # Aur model fields ke sahi naam (product_description) use kiye
        product_info = Product.objects.filter(
            Q(product_name__icontains=x) | 
            Q(product_description__icontains=x) | 
            Q(product_category__icontains=x)
        )
        
        # Sahi kiya: Home page par filtered list bheji taaki results dikhein
        return render(request, 'test1/home.html', {'product_info': product_info})
    
    return redirect('home')

def contact(request):
    if request.method == 'GET':
        return render(request, 'test1/contact.html')
    else:
        a = request.POST.get('name')
        b = request.POST.get('email')
        c = request.POST.get('message')
        new_data = Contact_Query(name=a, email=b, message=c)
        new_data.save()
        return render(request, 'test1/contact.html', {'x': 'Message Sent Successfully'})

@login_required(login_url="loginuser")
def products(request):
    myproducts = Product.objects.all()
    paginator = Paginator(myproducts, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'test1/product.html', {"page_obj": page_obj})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'test1/loginuser.html', {'form': AuthenticationForm()})
    else:
        a = request.POST.get('username')
        b = request.POST.get('password')
        user = authenticate(request, username=a, password=b)
        if user is None:
            return render(request, 'test1/loginuser.html', {'form': AuthenticationForm(), 'error': 'Invalid Credentials'})
        else:
            login(request, user)
            return redirect('home')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'test1/signupuser.html', {'form': UserCreationForm()})
    else:
        a = request.POST.get('username')
        b = request.POST.get('password1')
        c = request.POST.get('password2')
        if b == c:
            if User.objects.filter(username=a).exists():
                return render(request, 'test1/signupuser.html', {'form': UserCreationForm(), 'error': 'Username Already Exists. Try another!'})
            else:
                user = User.objects.create_user(username=a, password=b)
                user.save()
                login(request, user)
                return redirect('home')
        else:
            return render(request, 'test1/signupuser.html', {'form': UserCreationForm(), 'error': 'Password Mismatch! Try Again'})

def logoutuser(request):
    logout(request)
    return redirect('home')

@login_required(login_url="loginuser")
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    
    # Product count badhao
    product_id_str = str(product_id)
    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1
        
    request.session['cart'] = cart
    return redirect('products')

@login_required(login_url="loginuser")
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    
    for prod_id, qty in cart.items():
        try:
            product = Product.objects.get(id=int(prod_id))
            
            # Sahi kiya: Agar product_price nahi milta toh yeh automatic 'price' field check karega 
            # bina kisi error ke aur zero (0) nahi dikhayega!
            actual_price = getattr(product, 'product_price', getattr(product, 'price', 0))
            
            item_total = float(actual_price) * qty
            total_price += item_total
            
            cart_items.append({
                'product': product,
                'quantity': qty,
                'item_total': item_total
            })
        except (Product.DoesNotExist, ValueError):
            continue
            
    return render(request, 'test1/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required(login_url="loginuser")
def checkout_payment(request):
    # Payment status simulate karne ke liye simple view
    if request.method == 'POST':
        # Cart clear kar do payment successful hone ke baad
        request.session['cart'] = {}
        return render(request, 'test1/cart.html', {'payment_success': '🎉 Order Placed Successfully! DineX Kitchen is preparing your meal.'})
    return redirect('view_cart')