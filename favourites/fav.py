from shop.models import Product
from  django.conf import settings

class Favourite:

    def __init__(self,request):
        self.session = request.session
        fav = self.session.get(settings.FAVOURITE_SESSION_ID)
        if not fav:
            fav = self.session[settings.FAVOURITE_SESSION_ID] = {}
        self.fav = fav

    def add(self,product):
        product_id = str(product.id)
        if product_id not in self.fav:
            self.fav[product_id] = {'name':product.name}
            self.save()
    
    def save(self):
        self.session[settings.FAVOURITE_SESSION_ID] = self.fav
        self.session.modified = True
    

    def remove(self,product):
        product_id = str(product.id)
        if product_id in self.fav:
            del self.fav[product_id]
            self.save()
    def get_favourites(self):
        product_ids = self.fav.keys()
        return Product.objects.filter(id__in=product_ids)

    def clear(self):
        """Очистить все избранные товары"""
        self.session[settings.FAVOURITE_SESSION_ID] = {}
        self.session.modified = True

    def __len__(self):
        return len(self.fav)