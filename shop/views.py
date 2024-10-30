from django.shortcuts import render,get_object_or_404
from .models import Caterogy,Product
from cart.forms import CartAddProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from .forms import SearchForm
from django.contrib.postgres.search import TrigramSimilarity

def product_list(request,category_slug = None):
    category = None
    categories = Caterogy.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Caterogy,slug=category_slug)
        products = products.filter(category=category)
    return render(request,'shop/product/list.html',{'category':category,'categories':categories,'products':products})

@login_required
def product_detail(request,id,slug):
    product = get_object_or_404(Product,id=id,slug=slug,available=True)
    cart_product_form = CartAddProductForm()
    return render(request,'shop/product/detail.html',{'product':product,'cart_product_form':cart_product_form})

def home(request):
    return render(request,'shop/home.html')

def product_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Product.published.annotate(
                similarity=TrigramSimilarity('name', query),
            ).filter(similarity__gt=0.1).order_by('-similarity')
    return render(request,'shop/product/list.html',{'form':form,'query':query,'results':results})