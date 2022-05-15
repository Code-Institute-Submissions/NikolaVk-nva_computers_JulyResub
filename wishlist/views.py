from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from products.models import Product
from .models import Wishlist

# Create your views here.


def wishlist(request):
    lists = Wishlist.objects.filter(user_id=request.user.id)
    if lists.count()!=0:
        ourlist = lists.first()
        products = ourlist.list.all()
        print('products count: ' + products.count().__str__())

    context = {
        'wishlist': ourlist,
        'products': products,
    }

    return render(request, 'wishlist/wishlist.html', context)


@login_required
def add_wishlist(request, item_id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, pk=item_id)
    wishlist = Wishlist.objects.filter(user_id=request.user.id)
    
    redirect_url = request.POST.get('redirect_url')
    if wishlist.count() == 0:
        # add a new list
        wishListItem = Wishlist.objects.create(user=request.user)
    else:
        wishListItem = wishlist.first()
    if wishlist.count() != 1:
        messages.error(request, 'Unable to add product to wishlist')
    else:
        wishListItem.list.add(product)
        messages.success(request, f'Succesfully added {product.name} to wishlist!')

    return HttpResponseRedirect(url)


@login_required
def remove_wishlist(request, item_id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, pk=item_id)
    wishlist = Wishlist.objects.filter(user_id=request.user.id,list__id=product.id)
    
    redirect_url = request.POST.get('redirect_url')
    if wishlist.count() == 0:
        # Not on the list
        messages.error(request, 'Product is not on wishlist')
    else:
        wishListItem = wishlist.first()
        wishListItem.list.remove(product)
        messages.success(request, f'Succesfully removed {product.name} from wishlist!')


    return HttpResponseRedirect(url)
