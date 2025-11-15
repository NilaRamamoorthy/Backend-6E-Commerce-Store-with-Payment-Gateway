from django.shortcuts import render, redirect
from cart.views import get_cart_items_and_total
from django.contrib.auth.decorators import login_required
from django.conf import settings
import razorpay

@login_required
def checkout_view(request):
    cart_items, total = get_cart_items_and_total(request)
    
    if not cart_items:
        return redirect('cart_view')

    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    
    # Razorpay expects amount in paise
    razorpay_amount = int(total * 100)
    
    # Create an order in Razorpay
    razorpay_order = client.order.create({
        'amount': razorpay_amount,
        'currency': 'INR',
        'payment_capture': '1'
    })

    context = {
        'cart_items': cart_items,
        'total': total,
        'cart_count': sum(item['qty'] for item in cart_items),
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'razorpay_order_id': razorpay_order['id'],
        'amount': razorpay_amount,
        'currency': 'INR'
    }
    return render(request, 'checkout/checkout.html', context)

@login_required
def payment_success(request):
    # Clear cart after payment
    request.session['cart'] = {}
    return render(request, 'checkout/success.html')
