from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product

# Helper function to get cart from session
def get_cart(request):
    return request.session.get('cart', {})

# Helper function to calculate totals
def get_cart_items_and_total(request):
    cart = get_cart(request)
    items = []
    total = 0
    for product_id, qty in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * qty
        items.append({'product': product, 'qty': qty, 'subtotal': subtotal})
        total += subtotal
    return items, total

# View cart page
def cart_view(request):
    cart_items, total = get_cart_items_and_total(request)
    context = {
        'cart_items': cart_items,
        'total': total,
        'cart_count': sum(get_cart(request).values())
    }
    return render(request, 'cart/cart.html', context)

# Add to cart
def add_to_cart(request, product_id):
    cart = get_cart(request)
    product_id = str(product_id)
    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1
    request.session['cart'] = cart
    return redirect('cart_view')

# Decrease quantity
def decrease_cart(request, product_id):
    cart = get_cart(request)
    product_id = str(product_id)
    if product_id in cart:
        if cart[product_id] > 1:
            cart[product_id] -= 1
        else:
            cart.pop(product_id)
        request.session['cart'] = cart
    return redirect('cart_view')

# Remove item from cart
def remove_from_cart(request, product_id):
    cart = get_cart(request)
    product_id = str(product_id)
    if product_id in cart:
        cart.pop(product_id)
        request.session['cart'] = cart
    return redirect('cart_view')
