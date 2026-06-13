from itertools import product

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from store.models import Variation

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
    tax = 0
    grand_total = 0
    cart_items = []

    try:
        cart_obj = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart_obj, is_active=True)

        for item in cart_items:
            total += item.product.price * item.quantity
            quantity += item.quantity

        tax=(total * 0.02)
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total,
        'cart_items': cart_items,
    }
    return render(request, 'store/cart.html', context) #because cart template is in store folder

# -----------------------------
# ADD TO CART
# -----------------------------
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_variations = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            # print(f"{key}: {value}")
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variations.append(variation)
            except Variation.DoesNotExist:
                pass
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
    
    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

    if is_cart_item_exists:
        cart_item=CartItem.objects.filter(product=product, cart=cart)
        # existing variations -> database
        ex_var_list = []
        id = []

        for item in cart_item:
            existing_variation = item.variation.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)
            print(ex_var_list)

        # current variation -> product_variations
        if product_variations in ex_var_list:
            #increase the cart item quantity
            idx = ex_var_list.index(product_variations)
            item_id = id[idx]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else:
        # item_id -> database
            item = CartItem.objects.create(product=product, cart=cart, quantity=1)
            if len(product_variations) > 0:
                item.variation.clear()
                item.variation.add(*product_variations)
                item.save()

    else:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1,
        )
        if len(product_variations) > 0:
            cart_item.variation.clear()
            cart_item.variation.add(*product_variations)
            cart_item.save()

    return redirect('carts:cart')


# -----------------------------
# REMOVE FROM CART
# -----------------------------
def remove_from_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except ObjectDoesNotExist:
        pass
 
    return redirect('carts:cart')

# -----------------------------
# REMOVE ITEM FROM CART
# -----------------------------
def delete_cart_item(request, product_id,cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

        if cart_item.quantity >= 1:
            cart_item.delete()

    except ObjectDoesNotExist:
        pass

    return redirect('carts:cart')