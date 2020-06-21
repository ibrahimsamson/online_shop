from django.urls import path
from shopping.shop.views import (product_list,
                                 product_detail,
                                 cart_remove,
                                 cart_add,
                                 cart_detail
                                 )



app_name = 'shop'

urlpatterns = [
    path('', product_list, name='product_list'),
    path('<slug:category_slug>/', product_list,
         name='product_list_by_category'),
    path('cart/deta/ils', cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', cart_add, name='cart_add'),
    path('remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('<int:id>/<slug:slug>/', product_detail,
         name='product_detail'),

]
