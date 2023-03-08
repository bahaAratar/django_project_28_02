from rest_framework.test import APITestCase, APIRequestFactory
from django.contrib.auth import get_user_model
from .models import Order
from .views import OrderModelViewSet
from product.models import Product, Category
import uuid
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()

class OrderTest(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.setup_category()
        self.setup_product()
        self.setup_user()
        self.access_token = self.setup_user_token()

    @staticmethod
    def setup_category():
        category = [
            Category(title='cat1'),
            Category(title='cat2'),
            Category(title='cat3'),
        ]
        Category.objects.bulk_create(category)

    @staticmethod
    def setup_product():
        images = open('media/product/test.png', 'rb')
        product = [
            Product(category=Category.objects.first(), title='prod1', amount=20, price=20, image=images),
            Product(category=Category.objects.last(), title='prod2', amount=20, price=20, image=images),
            Product(category=Category.objects.first(), title='prod3', amount=20, price=20, image=images),
        ]
        Product.objects.bulk_create(product)

    def setup_user_token(self):
        data = {
            'email': 'test@test.com',
            'password': 'test123'
        }
        request = self.factory.post('account/login/', data)
        view = TokenObtainPairView.as_view()
        response = view(request)

        return response.data['access']

    def setup_user(self) -> None:
        self.user = User.objects.create_user(
            email='test@test.com',
            password='test123',
            is_active=True,
        )

    def test_order_post(self):
        data = {
            'product': Product.objects.first().id,
            'status': 'in_processing',
            'is_confirm': True,
            'amount': 20,
            'addres': 'ул. Пиздюкова, дом Скварцова',
            'number': 999999999,
            'total_price': 120.00,
            'activation_code': uuid.uuid4
        }
        
        request = self.factory.post('order/order', data, HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        view = OrderModelViewSet.as_view({'post': 'create'})
        response = view(request)

        print(response.status_code)
        print(response.data)
