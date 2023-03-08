from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from .models import Category, Product
from .views import CategoryAPIView, ProductModelViewSet
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()


class CategoryTest(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        category = [
            Category(title='cat1'),
            Category(title='cat2'),
            Category(title='cat3'),
        ]
        Category.objects.bulk_create(category)
        self.setup_user()

    def setup_user(self) -> None:
        self.user = User.objects.create_user(
            email='test@test.com',
            password='test123',
            is_active=True,
        )

    def test_get_category(self):
        request = self.factory.get('product/category')
        view = CategoryAPIView.as_view({'get': 'list'})
        response = view(request)
        # print(response.data)
        assert response.status_code == 200
        assert len(response.data) == 3
        assert response.data[0]['title'] == 'cat1'

    def test_post_category(self):
        data = {
            'title': 'cat4',
        }
        request = self.factory.post('product/category', data)
        force_authenticate(request, self.user)
        view = CategoryAPIView.as_view({'post': 'create'})
        response = view(request)
        # print(response.data)
        assert response.status_code == 201
        assert Category.objects.filter(title='cat4').exists()


class ProductTest(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.setup_category()
        self.setup_user()
        self.access_token = self.setup_user_token()

    def setup_user_token(self):
        data = {
            'email': 'test@test.com',
            'password': 'test123'
        }
        request = self.factory.post('account/login/', data)
        view = TokenObtainPairView.as_view()
        response = view(request)

        return response.data['access']

    @staticmethod
    def setup_category():
        category = [
            Category(title='cat1'),
            Category(title='cat2'),
            Category(title='cat3'),
        ]
        Category.objects.bulk_create(category)

    def setup_user(self) -> None:
        self.user = User.objects.create_user(
            email='test@test.com',
            password='test123',
            is_active=True,
        )

    def test_post_product(self):
        image = open('media/product/test.png', 'rb')
        # print(image)
        data = {
            # 'owner': self.user.id,
            'category': Category.objects.first(),
            'title': 'test_prod',
            'price': 20,
            'amount': 20,
            'image': image,
        }
        request = self.factory.post('product/product/', data, HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        # force_authenticate(request, self.user)

        view = ProductModelViewSet.as_view({'post': 'create'})
        response = view(request)
        # print(response.status_code)
        # print(response.data)
        assert response.status_code == 201
        assert Product.objects.filter(title='test_prod').exists()
