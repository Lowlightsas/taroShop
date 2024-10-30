from decimal import Decimal
from django.conf import settings
from shop.models import Product
from .models import CartItem  # Предполагается, что у вас есть эта модель для хранения товаров корзины

class Cart:

    def __init__(self, request):
        self.session = request.session
        self.user = request.user  # Добавлено для определения пользователя
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=0, override_quantity=False):
        product_id = str(product.id)
        if self.user.is_authenticated:
            # Для авторизованных пользователей сохраняем в базе данных
            cart_item, created = CartItem.objects.get_or_create(
                user=self.user, product=product
            )
            if override_quantity:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity
            cart_item.save()
        else:
            # Для неавторизованных пользователей сохраняем в сессии
            if product_id not in self.cart:
                self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
            if override_quantity:
                self.cart[product_id]['quantity'] = (quantity-1)
            else:
                self.cart[product_id]['quantity'] += (quantity - 1)
            self.save()

    def save(self):
        # Сохраняем изменения в сессии
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        if self.user.is_authenticated:
            # Удаляем из базы данных для авторизованных пользователей
            CartItem.objects.filter(user=self.user, product=product).delete()
        else:
            # Удаляем из сессии для неавторизованных пользователей
            product_id = str(product.id)
            if product_id in self.cart:
                del self.cart[product_id]
                self.save()

    def __iter__(self):
        if self.user.is_authenticated:
            # Для авторизованных пользователей данные из базы данных
            cart_items = CartItem.objects.filter(user=self.user).select_related('product')
            for item in cart_items:
                yield {
                    'product': item.product,
                    'quantity': item.quantity,
                    'price': item.product.price,
                    'total_price': item.quantity * item.product.price
                }
        else:
            # Для неавторизованных пользователей данные из сессии
            product_ids = self.cart.keys()
            products = Product.objects.filter(id__in=product_ids)
            cart = self.cart.copy()
            for product in products:
                cart[str(product.id)]['product'] = product
            for item in cart.values():
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['quantity']
                yield item

    def __len__(self):
        if self.user.is_authenticated:
            # Количество для авторизованных пользователей
            return sum(item.quantity for item in CartItem.objects.filter(user=self.user))
        else:
            # Количество для неавторизованных пользователей
            return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        if self.user.is_authenticated:
            # Общая сумма для авторизованных
            return sum(item.quantity * item.product.price for item in CartItem.objects.filter(user=self.user))
        else:
            # Общая сумма для неавторизованных
            return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        if self.user.is_authenticated:
            # Очищаем корзину в базе данных для авторизованных
            CartItem.objects.filter(user=self.user).delete()
        else:
            # Очищаем корзину в сессии для неавторизованных
            del self.session[settings.CART_SESSION_ID]
            self.save()
