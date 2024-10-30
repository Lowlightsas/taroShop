from django.db import models
from django.conf import settings
from shop.models import Product

class FavouriteModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user','product')
    
    def __str__(self):
        return f'{self.user.username} - {self.product.name}'