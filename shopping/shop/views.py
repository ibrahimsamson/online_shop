from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from shopping.shop.models import Category, Product
from shopping.shop.cart import Cart
from shopping.shop.forms import CartAddProductForm


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        return render(request,
                       'shop/list.html',
                       {'category':category,
                        'categories':Categories,
                        'products': products})
    else:
        return render(request, 'shop/list.html',
                      {'categories':categories,
                      'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/details',
                  {'Product':product,
                   'cart_product_form':cart_product_form})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
        return redirect('shop:cart_detail')
    else :
        return form


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('shop:cart_detail')


def cart_detail(request):
    cart = Cart(request)

    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                    initial={'quantity': item['quantity'],
                             'update':True})

    return render(request, 'cart/detail.html', {'cart': cart})
