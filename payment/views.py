from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from .forms import ShippingAddressForm, BillingForm
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from ecommerceApp.models import Product, Category, Profile
from .sendEmail import send_order_notification
from django.core.mail import send_mail
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags
from django.conf import settings
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import pdfkit
import datetime
# Create your views here.
def billing_info(request):

    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_products
        quantities = cart.get_qtys
        total = cart.cart_total()
        total_items = cart.total_items()
        categories = Category.objects.all()  # Get all categories
    

        # create session with shipping info 'we can take this in other views' -> like pricess order
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
        
        if request.user.is_authenticated:
            # Get the billing form    
            billing_form = BillingForm()

            shipping_info = request.POST
            context = {
                'cart_products':cart_products,
                'quantities':quantities,
                'total':total,
                'total_items':total_items,
                'shipping_info': shipping_info,
                'billing_form':billing_form,
                'categories':categories,
                }
            return render(request, 'eCommerce/billing_info.html', context)
        else:
            billing_form = BillingForm()
            shipping_info = request.POST
            context = {
                'cart_products':cart_products,
                'quantities':quantities,
                'total':total,
                'total_items':total_items,
                'shipping_info': shipping_info,
                'billing_form':billing_form,
                'categories':categories,
                }
            return render(request, 'eCommerce/billing_info.html', context)

        shipping_info = request.POST
        return render(request, 'eCommerce/billing_info.html', {'shipping_info':shipping_info})
    
    else:
        messages.error(request, "Access denied")
        return redirect('main')

def create_order_confirmation_email(order):
    # Define context for rendering the email template
    context = {
        'order': order,
        'delivery_date': order.date_shipped.strftime("%B %d, %Y") if order.date_shipped else "Not specified",
    }
    
    # Render the email template with context
    email_html = render_to_string('payment/order_confirmation_email.html', context)
    
    # Optionally, strip HTML tags for the plain text email
    email_plain = strip_tags(email_html)
    
    return email_plain, email_html
    
def process_order(request):
    
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_products
        quantities = cart.get_qtys
        total = cart.cart_total()
        total_items = cart.total_items()

        
        #get the billing info from the last page (billing info 'method')  
        payment_form = BillingForm(request.POST or None) #--> 
        # get shipping session
        my_shipping = request.session.get('my_shipping') # --> btrga3li kl m3lomat al shipping 
        """
        {'csrfmiddlewaretoken': 'H85NpZrcDwMozrXr2Q4BLeYEXH631nBPt3z0Bh8GQhye83YJMwim8E88DSacIkFt',
        'shipping_full_name': '\u202aM7md Tamer\u202c\u200f', 'shipping_email': 'mohamed55555ta@gmail.com', 
        'shipping_address1': 'ميت غمر', 'shipping_address2': '', 'shipping_country': 'Egypt', 
        'shipping_city': 'Daqahilya', 'shipping_state': 'الإسماعيلية'}
        """

        # create shipping address "that was TextFeild in Order model" from our session "my_shipping"
        full_name = my_shipping['shipping_full_name']
        shipping_address = f"{my_shipping['shipping_full_name']}\n{my_shipping['shipping_email']}\n{my_shipping['shipping_phone']}\n{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_country']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}"
        email = my_shipping['shipping_email']
        phone = my_shipping['shipping_phone']
        amount_paid = total

        if request.user.is_authenticated:

            user = request.user

            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid, phone=phone, quantity=total_items)
            create_order.save()
            
            order_id = create_order.pk

            for product in cart_products():
                product_id = product.id

                if product.is_sale :
                    price = product.sale_price
                else:
                    price = product.price    

                for key, value in quantities().items():
                    if int(key) == product_id:
                        qprice = price*value #---> get all product's price price*quantity
                        create_order_item = OrderItem(user=user, order_id= order_id, product_id=product_id, price = qprice, quantity=value)  
                        create_order_item.save()

            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]   

            # delete current cart (old_cart field)
            current_user = Profile.objects.filter(user__id=request.user.id) 
            current_user.update(old_cart='')          

            email_plain, email_html = create_order_confirmation_email(create_order)
        
            # Send email using Django's send_mail function
            subject = 'Order Confirmation'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [create_order.email]  # Send to the customer's email address
            
            send_mail(subject, email_plain, from_email, to_email, html_message=email_html)
            send_order_notification(create_order)
            messages.success(request, 'Order placed')
            return redirect('main')

        else:

            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid, phone=phone, quantity=total_items)
            create_order.save()
            order_id = create_order.pk

            for product in cart_products():
                product_id = product.id

                if product.is_sale :
                    price = product.sale_price
                else:
                    price = product.price    

                for key, value in quantities().items():
                    if int(key) == product_id:
                        qprice = price*value #---> get all product's price price*quantity
                        create_order_item = OrderItem(order_id= order_id, product_id=product_id, price = qprice, quantity=value)  
                        create_order_item.save()

            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

            email_plain, email_html = create_order_confirmation_email(create_order)
        
            # Send email using Django's send_mail function
            subject = 'Order Confirmation'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [create_order.email]  # Send to the customer's email address
            
            send_mail(subject, email_plain, from_email, to_email, html_message=email_html)
            send_order_notification(create_order)

            messages.success(request, 'Order placed')
            return redirect('main')
        
        
    else:
        messages.error(request, "Access denied")
        return redirect('main')


def shipped_dash(request):
    categories = Category.objects.all()  # Get all categories
    cart = Cart(request)  # Get the current cart
    total_items = cart.total_items()  # Get total items in the cart

    if request.user.is_authenticated and request.user.is_superuser :
        orders = Order.objects.filter(shipped=True)

        paginator = Paginator(orders, 10)  # Show 10 orders per page
        page = request.GET.get('page')

        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except EmptyPage:
            orders = paginator.page(paginator.num_pages)
            
        if request.POST :
            shipped_status = request.POST["shipped_status"]
            num = request.POST["num"]
            
            order = Order.objects.filter(id=num)
            order.update(shipped=False)
            messages.success(request, "Status updated")
            return redirect('shipped_dash')
                

        return render(request, 'eCommerce/shipped_dash.html', {'orders':orders , 'categories': categories,'total_items': total_items,})

    else :

        messages.error(request, "Access denied")
        return redirect('main')    

def create_shipped_confirmation_email(order):
    context = {
        'order': order,
        'delivery_date': order.date_shipped.strftime("%B %d, %Y") if order.date_shipped else "Not specified",
    }
    email_html = render_to_string('payment/shipped_confirmation_email.html', context)
    email_plain = strip_tags(email_html)
    return email_plain, email_html

def not_shipped_dash(request):
    categories = Category.objects.all()  # Get all categories
    cart = Cart(request)  # Get the current cart
    total_items = cart.total_items()  # Get total items in the cart

    if request.user.is_authenticated and request.user.is_superuser :
        orders = Order.objects.filter(shipped=False)

        paginator = Paginator(orders, 10)  # Show 10 orders per page
        page = request.GET.get('page')

        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except EmptyPage:
            orders = paginator.page(paginator.num_pages)

        if request.POST :
            shipped_status = request.POST["shipped_status"]
            num = request.POST["num"]   
            order = Order.objects.get(id=num)
            now = datetime.datetime.now()
            # order_was_shipped = Order.objects.get(id=num)
            order.shipped = True
            order.date_shipped = now
            order.save()
            messages.success(request, "Status updated")
            email_plain, email_html = create_shipped_confirmation_email(order)
        
            # Send email using Django's send_mail function
            subject = 'تم شحن اوردرك'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [order.email]  # Send to the customer's email address
            
            send_mail(subject, email_plain, from_email, to_email, html_message=email_html)
            send_order_notification(order)
            return redirect('not_shipped_dash') 

        return render(request, 'eCommerce/not_shipped_dash.html', {'orders':orders, 'categories': categories,'total_items': total_items,})


    else :

        messages.error(request, "Access denied")
        return redirect('main')   

def order(request, pk):
    categories = Category.objects.all()  # Get all categories
    cart = Cart(request)  # Get the current cart
    total_items = cart.total_items()  # Get total items in the cart

    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.get(id=pk)

        order_items = OrderItem.objects.filter(order=pk)

        if request.POST :
            shipped_status = request.POST["shipped_status"]

            if shipped_status == "false":
                order = Order.objects.filter(id=pk)
                order.update(shipped=False)
                messages.success(request, "Status updated")
                return redirect('shipped_dash')
                
                
            else:    
                order = Order.objects.filter(id=pk)
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
                messages.success(request, "Status updated")
                return redirect('not_shipped_dash')
                
        
        return render(request, 'eCommerce/order.html', {'orders':orders, 'order_items':order_items, 'categories': categories,'total_items': total_items,})
    else:
        messages.error(request, "Access denied")
        return redirect('main')

def payment_success(request):
    return render(request, 'payment/payment_success.html', {})

def checkout(request):

    cart = Cart(request)
    cart_products = cart.get_products
    quantities = cart.get_qtys
    total = cart.cart_total()
    total_items = cart.total_items()
    categories = Category.objects.all()  # Get all categories
    

    # add shipping form

    if request.user.is_authenticated:
        # Get the current user's shipping information
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        shipping_form = ShippingAddressForm(request.POST or None, instance=shipping_user)

        context = {
        'cart_products':cart_products,
        'quantities':quantities,
        'total':total,
        'total_items':total_items,
        'shipping_form': shipping_form,
        'categories': categories,
        }
        return render(request, 'eCommerce/checkout.html', context)

    else :

        shipping_form = ShippingAddressForm(request.POST or None)

        context = {
            'cart_products':cart_products,
            'quantities':quantities,
            'total':total,
            'total_items':total_items,
            'shipping_form': shipping_form,
            'categories': categories,
        }
        return render(request, 'eCommerce/checkout.html', context)
    

def generate_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    delivery_date = order.date_shipped.strftime("%B %d, %Y") if order.date_shipped else "غير محدد"
    
    context = {
        'order': order,
        'order_items': order_items,
        'delivery_date': delivery_date,
    }
    
    html_string = render_to_string('payment/order_pdf.html', context)
    
    try:
        pdf = pdfkit.from_string(html_string, False, configuration=settings.PDFKIT_CONFIG)
    except Exception as e:
        return HttpResponse(f"Error generating PDF: {e}", status=500)
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="order_{order_id}.pdf"'
    
    return response