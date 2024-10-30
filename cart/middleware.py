from .cart import Cart
from shop.models import Product

class MergeCartMiddleware:
    """
    
    Middleware для объединения корзины из сессии и базы данных при авторизации.
    
    """
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        if request.user.is_authenticated:
            cart = Cart(request)
            if request.session.get('cart'):
                for item in cart.cart.values():
                    product = Product.objects.get(id=item['product'])
                    cart.add(product,item['quantity'],override_quantity=False)
                cart.clear()
        response = self.get_response(request)
        return response