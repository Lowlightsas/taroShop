from django.shortcuts import render,redirect,get_object_or_404
from .fav import Favourite
from shop.models import Product

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def add_to_fav(request, product_id):
    if request.method=="POST":
        fav = Favourite(request)
        product = get_object_or_404(Product, id=product_id)
        fav.add(product)
        return JsonResponse({"status": "success"})
    return redirect("shop:list")

@login_required
def remove_to_fav(request,product_id):
    fav = Favourite(request)
    product = get_object_or_404(Product,id=product_id)
    fav.remove(product)
    return redirect('favourites:all')

@login_required
def clear(request):
    fav = Favourite(request)
    fav.clear()
    return redirect('favourites:all')

@login_required
def all(request):
    fav = Favourite(request)
    products = fav.get_favourites()
    return render(request,'favourites/list.html',{'products':products})
