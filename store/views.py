from django.shortcuts import render, redirect
from .models import Product

def home(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    # Cart count for badge
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values()) if cart else 0

    context = {
        'products': products,
        'cart_count': cart_count
    }
    return render(request, 'store/home.html', context)
