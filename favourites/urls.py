from django.urls import path
from . import views

app_name = 'favourites'


urlpatterns = [
    path('all/',views.all,name='all'),
    path('clear/',views.clear,name='clear'),
    path('favourites/add_to_fav/<int:product_id>/', views.add_to_fav, name='add_to_fav'),
    path('favourites/remove_to_fav/<int:product_id>/', views.remove_to_fav, name='remove_to_fav'),
    
]
