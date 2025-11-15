from django.http import JsonResponse
from django.shortcuts import render, redirect
from store.models import Product

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    # Add or increment quantity
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1  

    request.session['cart'] = cart
    request.session.modified = True
    
    return redirect('cart_view')  # redirect to cart page


from django.shortcuts import render
from store.models import Product

def cart_view(request):
    cart = request.session.get('cart', {})

    cart_items = []
    total = 0

    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.price * qty
        total += subtotal
        cart_items.append({
            'product': product,
            'qty': qty,
            'subtotal': subtotal
        })

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total': total
    })
