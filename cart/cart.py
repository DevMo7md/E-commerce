from ecommerceApp.models import Product, Profile
from decimal import Decimal
class Cart():
    def __init__(self, request):
        self.session = request.session

        self.request = request

        # get the current session key if it exist
        cart = self.session.get('session_key')
        # if user is new, don't have session key --> creat one!
        if 'session_key' not in request.session :
            cart = self.session['session_key'] = {}

        # make sure cart is avilable in all pages
        self.cart = cart

    def add(self, product, quantity):
        # get the product id
        product_id = str(product.id)
        product_qty= str(quantity)
        
        # logic
        if product_id in self.cart :
            pass
        else :
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

        if self.request.user.is_authenticated:
            # get current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convert {'1':3, '4':5} to {"1":3, "4":5}
            carty = str(self.cart)
            carty = carty.replace("'", '"')
            #save carty in old_cart
            current_user.update(old_cart=str(carty))

    def db_add(self, product, quantity):
        # get the product id
        product_id = str(product)
        product_qty= str(quantity)
        
        # logic
        if product_id in self.cart :
            pass
        else :
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

        if self.request.user.is_authenticated:
            # get current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convert {'1':3, '4':5} to {"1":3, "4":5}
            carty = str(self.cart)
            carty = carty.replace("'", '"')
            #save carty in old_cart
            current_user.update(old_cart=str(carty))        


    def cart_total(self):

        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in = product_ids)

        qtys = self.cart
        # {'1':4, '2':6} --> key is id and value is quantity
        total = Decimal(0) # start quantity from 0
        for key, value in qtys.items():
            key = int(key) # convert key from string to integer
            for product in products :
                if product.id == key:
                    if product.is_sale :
                        total = total + (Decimal(product.sale_price)*Decimal(value))
                    else:    
                        total = total + (Decimal(product.price)*Decimal(value))
        return total
    

    def total_items (self):
        prodict_ids = self.cart.keys()
        products = Product.objects.filter(id__in=prodict_ids)

        qtys = self.cart 
        total = 0
        for key, value in qtys.items():
            key = int(key)
            for product in products :
                if product.id == key :
                    total = total + int(value)
        return total            



    def __len__(self):
        return len(self.cart)   


    def get_products(self):
        product_ids = self.cart.keys()
        
        products = Product.objects.filter(id__in=product_ids)

        return products
    
    def get_qtys(self):
        qtys = self.cart

        return qtys

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        ourcart = self.cart
        ourcart[product_id] = int(product_qty)

        self.session.modified = True

        if self.request.user.is_authenticated:
            # get current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convert {'1':3, '4':5} to {"1":3, "4":5}
            carty = str(self.cart)
            carty = carty.replace("'", '"')
            #save carty in old_cart
            current_user.update(old_cart=str(carty))

        thing = self.cart
        return thing


    def delete(self, product):
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True   

        if self.request.user.is_authenticated:
            # get current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convert {'1':3, '4':5} to {"1":3, "4":5}
            carty = str(self.cart)
            carty = carty.replace("'", '"')
            #save carty in old_cart
            current_user.update(old_cart=str(carty)) 