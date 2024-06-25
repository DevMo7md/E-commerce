from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import UpdateUserForm, UpdatePwForm, UpdateInfoForm
from payment.forms import ShippingAddressForm
from payment.models import ShippingAddress
from django.db.models import Q
import json

# Create your views here.

# View for the store's main page
def store(request):
    
    products = Product.objects.all()  # Get all products
    categories = Category.objects.all()  # Get all categories
    cart = Cart(request)  # Get the current cart
    total_items = cart.total_items()  # Get total items in the cart
    product = None
    err = None

    # Check if there is a search query
    if 'search-bar' in request.GET:
        product = request.GET['search-bar']
        if product:
            # Filter products based on the search query
            products = products.filter(Q(name__icontains=product) | Q(description__icontains=product))
            if not products:
                err = f'No results for {product} \n Try checking your spelling or use more general terms'

    context = {
        'products': products,
        'product':product,
        'categories': categories,
        'err_message': err,
        'total_items': total_items,
    }
    return render(request, 'eCommerce/main.html', context)  # Render the store template

# View for a specific product page
def products(request, pk):

    product = Product.objects.get(id=pk)  # Get the product by ID
    categories = Category.objects.all()  # Get all categories
    cart = Cart(request)  # Get the current cart
    total_items = cart.total_items()  # Get total items in the cart
    context = {
        'product': product,
        'categories': categories,
        'total_items': total_items,
    }
    return render(request, 'eCommerce/product.html', context)  # Render the product template

# View for products by category
def category(request, foo):

    foo = foo.replace('-', ' ')  # Replace dashes with spaces
    cart = Cart(request)  # Get the current cart
    total_items = cart.total_items()  # Get total items in the cart

    try:
        category = Category.objects.get(name=foo)  # Get the category by name
        categories = Category.objects.all()  # Get all categories
        products = Product.objects.filter(category=category)  # Get products in the category
        return render(request, 'eCommerce/category.html', {'products': products, 'category': category, 'categories': categories, 'total_items': total_items})  # Render the category template
    except:
        messages.success(request, "That category doesn't exist!")
        return redirect('main')  # Redirect to main page if category doesn't exist

# View for the about page
def about(request):

    return render(request, 'eCommerce/about.html')  # Render the about template

# View to add a product to the cart
def cart_add(request):

    cart = Cart(request)  # Get the current cart

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))  # Get product ID from POST data
        product = get_object_or_404(Product, id=product_id)  # Get the product by ID
        cart.add(product=product)  # Add the product to the cart
        cart_quantity = cart.__len__()  # Get the number of items in the cart
        response = JsonResponse({'quantity: ': cart_quantity})  # Return the cart quantity as JSON
        return response

# View to update the user's password
def update_pw(request):

    cart = Cart(request)  # Get the current cart
    total_items = cart.total_items()  # Get total items in the cart
    categories = Category.objects.all()  # Get all categories
    

    if request.user.is_authenticated:
        if request.method == 'POST':
            current_user = request.user
            old_password = request.POST.get('old_password')
            form = UpdatePwForm(current_user, request.POST)

            if not current_user.check_password(old_password):
                messages.error(request, "Sorry, your old password not matched with your password")
                return redirect('update_pw')

            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Maintain session after password change
                messages.success(request, "Password has been updated!")
                return redirect('main')
            else:
                for err in list(form.errors.values()):
                    messages.error(request, err)
                return redirect('update_pw')
        else:
            form = UpdatePwForm(request.user)
            return render(request, 'eCommerce/update_pw.html', {'form': form, 'total_items': total_items, 'categories': categories})
    else:
        messages.error(request, "Sorry, you must be logged in")
        return redirect('main')

# View to update user details
def update_user(request):

    cart = Cart(request)  # Get the current cart
    total_items = cart.total_items()  # Get total items in the cart
    categories = Category.objects.all()  # Get all categories
    

    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, "User has been updated Successfully!")
            return redirect('main')
        return render(request, 'eCommerce/update_user.html', {'user_form': user_form, 'total_items': total_items, 'categories':categories})
    else:
        messages.error(request, "Sorry, This action needs user logged in !")
        return redirect('main')

# View to register a new user
def register_user(request):

    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first-name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name)
                user.save()
                login(request, user)
                messages.success(request, 'Your account has been created successfully, Please complete your data')
                return redirect('update_profile')
        else:
            messages.error(request, 'Passwords do not match')
    return render(request, 'eCommerce/register.html')  # Render the registration template

# View to login a user
def login_user(request):

    if request.method == 'POST':
        username = request.POST['usernamee']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #get the current user
            current_user = Profile.objects.get(user__id=request.user.id)
            # get old cart 
            saved_cart = current_user.old_cart

            if saved_cart:
                # convert cart from string to python dictionary with json 
                converted_cart = json.loads(saved_cart) #--> {"2":1, "3":4}
                cart = Cart(request)
                #add the load cart to our session
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)



            messages.success(request, "You successfully logged in")
            return redirect('main')
        else:
            messages.warning(request, "Username or password is wrong, please try again")
            return redirect('login')
    else:
        return render(request, 'eCommerce/login.html')  # Render the login template

# View to logout a user
def logout_user(request):

    logout(request)
    messages.success(request, 'You are successfully logged out')
    return redirect('main')  # Redirect to main page after logout


# add, update user info
def update_profile(request):
    cart = Cart(request)  # Get the current cart
    total_items = cart.total_items()  # Get total items in the cart
    categories = Category.objects.all()  # Get all categories


    if request.user.is_authenticated:
        # Get the current user
        current_user = Profile.objects.get(user__id=request.user.id)
        # Get the current user's shipping information
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        form = UpdateInfoForm(request.POST or None, instance=current_user)

        shipping_form = ShippingAddressForm(request.POST or None, instance=shipping_user)

        if request.method == 'POST':

            if form.is_valid() or shipping_form.is_valid():
                # Save original form
                form.save()
                # Save shipping form
                shipping_form.save()

                messages.success(request, "User informations has been updated Successfully!")
                return redirect('main')
        return render(request, 'eCommerce/update_prof.html', {'form': form, 'total_items': total_items, 'shipping_form':shipping_form, 'categories':categories})
    else:
        messages.error(request, "Sorry, This action needs user logged in !")
        return redirect('main')
