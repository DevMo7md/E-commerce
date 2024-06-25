from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from ecommerceApp.models import Product
from django.http import JsonResponse
from django.contrib import messages
from ecommerceApp.models import Category

# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_products
    cart_quantities = cart.get_qtys
    total = cart.cart_total()
    total_items = cart.total_items()
    categories = Category.objects.all()  # Get all categories
    
    context = {'cart_products': cart_products, 'cart_quantities':cart_quantities, 'total':total, 'total_items':total_items, 'categories':categories }
    return render(request, 'cart/cart_summary.html', context)

def cart_add(request):
    
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = request.POST.get('product_qty')
        if product_qty is None:
            return JsonResponse({'error': 'Product quantity is missing'}, status=400)

        try:
            product_qty = int(product_qty)
        except ValueError:
            return JsonResponse({'error': 'Invalid product quantity'}, status=400)


        product = get_object_or_404(Product, id=product_id)

        cart.add(product=product, quantity=product_qty)

        cart_quantity = cart.__len__()
        # response = JsonResponse({'product name: ': product.name})
        response = JsonResponse({'quantity: ': cart_quantity})
        messages.success(request, "Product added successfuly!")
        return response



def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = request.POST.get('product_qty')
        if product_qty is None:
            return JsonResponse({'error': 'Product quantity is missing'}, status=400)

        try:
            product_qty = int(product_qty)
        except ValueError:
            return JsonResponse({'error': 'Invalid product quantity'}, status=400)


        cart.update(product=product_id, quantity=product_qty)
        response = JsonResponse({'qty': product_qty})
        messages.success(request, "Quantity updated succesfuly!")
        return response
        #return redirect('cart_summary')

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        

        cart.delete(product=product_id)
        response = JsonResponse({'product': product_id})
        messages.success(request, "Product deleted successfuly!")
        return response
        #return redirect('cart_summary')
