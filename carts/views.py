from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction

from store.models import Product
from .models import Cart, CartItem


# -----------------------------
# CART SESSION HELPER
# -----------------------------
def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


def get_cart(request):
    """
    Returns existing cart or creates a new one.
    """
    cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))
    return cart


# -----------------------------
# VIEW: CART PAGE
# -----------------------------
def cart(request):
    total = 0
    quantity = 0
    cart_items = []

    try:
        cart_obj = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart_obj, is_active=True)

        for item in cart_items:
            total += item.product.price * item.quantity
            quantity += item.quantity

        tax=(total * 0.02)
        grand_total = total + tax
    except Cart.DoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total,
        'cart_items': cart_items,
    }
    return render(request, 'store/cart.html', context)


# -----------------------------
# ADD TO CART
# -----------------------------
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)

    cart_item, created = CartItem.objects.get_or_create(
        product=product,
        cart=cart,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('carts:cart')


# -----------------------------
# REMOVE FROM CART
# -----------------------------
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    except CartItem.DoesNotExist:
        pass

    return redirect('carts:cart')

# -----------------------------
# REMOVE ITEM FROM CART
# -----------------------------
def delete_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)

        if cart_item.quantity >= 1:
            cart_item.delete()

    except CartItem.DoesNotExist:
        pass

    return redirect('carts:cart')