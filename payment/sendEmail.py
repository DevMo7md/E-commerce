from django.core.mail import send_mail
from django.conf import settings

def send_order_notification(order):
    subject = f"New Order #{order.id}"
    order_items = order.order_items.all()  # Use 'order_items' instead of 'order_item'  # Assuming 'OrderItem' has a ForeignKey to 'Order' named 'order'
    
    item_list = ""
    for item in order_items:
        item_list += f"{item.product.name} - Quantity: {item.quantity} - Price: ${item.price}\n   "


    message = f"""
    You have a new order!
    
    Order ID: {order.id}
    Customer: {order.full_name}
    Email: {order.email}
    Phone: {order.phone}
    Total: ${order.amount_paid}

    Products: \n
        {item_list}

    Shipping Address:
    {order.shipping_address}
    """
    recipient_list = ['mohammed5555ta@gmail.com', 'mohamed55555ta@gmail.com']  # Admin email

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
