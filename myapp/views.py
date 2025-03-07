from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone  # Add this import
from .models import Category, Product, Order
from .forms import OrderForm, InterestForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime, timedelta
# Index View (No changes)

def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]  # Fetch categories
    return render(request, 'myapp/index.html', {'cat_list': cat_list})

    # response = HttpResponse()
    # response.write("<h2>List of Categories:</h2>")
    # for category in cat_list:
    #     response.write(f"<p>{category.id}: {category.name}</p>")
    #
    # response.write("<h2>Top 5 Most Expensive Products:</h2>")
    # for product in product_list:
    #     response.write(f"<p>{product.name} - ${product.price}</p>")
    #
    # return response

# About View (Restored to its original version)
# def about(request):
#      return render(request, 'myapp/about0.html')
def about(request):
    return render(request, 'myapp/about.html')

# Category Detail View - Improved formatting
# def detail(request, cat_no):
#      category = get_object_or_404(Category, id=cat_no)
#      return render(request, 'myapp/detail.html', {'category': category})

def detail(request, cat_no):
    category = get_object_or_404(Category, id=cat_no)
    return render(request, 'myapp/detail.html', {'category': category})

def products(request):
    # Display all products
    prodlist = Product.objects.all().order_by('id')[:10]  # Get first 10 products
    return render(request, 'myapp/products.html', {'prodlist': prodlist})

def place_order(request):
    """View for placing orders"""
    msg = ''  # Initialize message
    prodlist = Product.objects.all()  # Get all products
    
    if request.method == 'POST':  # Form was submitted
        form = OrderForm(request.POST)
        if form.is_valid():  # Check if valid
            order = form.save(commit=False)  # Create order but don't save yet
            if order.num_units <= order.product.stock:  # Check stock
                 # Set the order date to current date
                order.order_date = timezone.now().date()
                # Save the order
                order.save()
                
                # Update the stock (important!)
                product = order.product
                product.stock -= order.num_units
                product.save()
                
                msg = 'Your order has been placed successfully.'
            else:
                msg = 'We do not have sufficient stock to fill your order.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:  # GET request - show empty form
        form = OrderForm()
    
    return render(request, 'myapp/placeorder.html', {
        'form': form, 
        'msg': msg, 
        'prodlist': prodlist
    })
    
def productdetail(request, prod_id):
    #Display details about a specific product
    product = get_object_or_404(Product, id=prod_id)  # Get product or 404
    
    if request.method == 'POST':  # Form submitted
        form = InterestForm(request.POST)
        if form.is_valid():
            interested = form.cleaned_data['interested']
            if int(interested) == 1:  # If user selected "Yes"
                product.interested += 1  # Increment interest counter
                product.save()
            return redirect('myapp:index')  # Redirect to index page
    else:  # GET request
        form = InterestForm()  # Empty form
    
    return render(request, 'myapp/productdetail.html', {
        'product': product,
        'form': form,
        'available': product.available  # Pass if product is available
    })

# Add these functions to views.py
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                # Part 2, Step a: Store login timestamp in session
                current_login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                request.session['last_login'] = current_login_time
                # Set session to expire in 1 hour
                request.session.set_expiry(3600)  # 3600 seconds = 1 hour
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))

@login_required
def myorders(request):
    if hasattr(request.user, 'client'):
        # User is a Client, get their orders
        orders = Order.objects.filter(client=request.user.client)
        return render(request, 'myapp/myorders.html', {'orders': orders})
    else:
        # User is not a Client
        return render(request, 'myapp/myorders.html',
                     {'message': 'You are not a registered client!'})


def about(request):
    # Check for an existing cookie
    visits = 1
    if 'about_visits' in request.COOKIES:
        # Get existing value and increment
        visits = int(request.COOKIES['about_visits']) + 1

    # Render the template with the visit count
    response = render(request, 'myapp/about.html', {'visits': visits})

    # Set/update the cookie to expire in 5 minutes (300 seconds)
    response.set_cookie('about_visits', visits, max_age=300)

    return response


def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]  # Fetch categories

    # Check if last_login exists in session
    last_login = None
    if 'last_login' in request.session:
        last_login = request.session['last_login']

    context = {
        'cat_list': cat_list,
        'last_login': last_login
    }

    return render(request, 'myapp/index.html', context)

