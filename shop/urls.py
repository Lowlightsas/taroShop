from . import views
from django.urls import path

app_name = 'shop'


urlpatterns = [
    path('',views.home,name='home'),
    path('search/',views.product_search,name='search'),
    path('list/',views.product_list,name='list'),
    path('<slug:category_slug>/',views.product_list,name='product_list_by_category'),
    path('<int:id>/<slug:slug>/',views.product_detail,name='product_detail'),
  
]