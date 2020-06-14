from django.shortcuts import render, get_object_or_404
from shopping.shop.models import Category, Product


def product_list(request, category_slug=None):
    category = None
    categories = Category.object.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        return render (request,
                       'shop/products/list.html',
                       {'category':category,
                        'categories':Categories,
                        'products': products})

def product_details(request, id, slug):
    product = get_object_or_404(id=id,
                                slug=slug,
                                available=True)
    return render(request, 'shop/products/details',
                  {'Product':product})



