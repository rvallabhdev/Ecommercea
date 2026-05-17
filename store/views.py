from django.shortcuts import render

from carts.views import _cart_id
from category.models import Category
from .models import Product
from django.shortcuts import get_object_or_404
from carts.models import CartItem
from carts.views import _cart_id

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(is_available=True, category=categories)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()

    for product in products:
        rounded_price = round((product.price * 1.25) / 50) * 50
        product.old_price = rounded_price - 1

    #Examples:
    # 200 → 199
    # 150 → 149
    # 350 → 349
    
    # So first:
    # increase by 25%
    # round to nearest 50
    # subtract 1

    product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    
    rounded_price = round((single_product.price * 1.25) / 50) * 50
    single_product.old_price = rounded_price - 1

    context = {
        'single_product': single_product,
        'single_product_old_price': single_product.old_price,
    }

    return render(request, 'store/product_detail.html', context)
