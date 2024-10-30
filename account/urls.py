from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
app_name = 'account'

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(next_page='shop:home'), name='logout'),
    path('', include('django.contrib.auth.urls')),
    path('register/',views.register,name='register'),
    path('edit/',views.edit,name='edit'),
    path('profile/',views.profile,name='profile'),
    path('order_list/',views.order_list,name='order_list'),
   
]
