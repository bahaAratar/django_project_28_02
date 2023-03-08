from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics, viewsets
from .models import Product, Category
from .tasks import big_func
from .serializer import ProductSerializer, CategorySerializer


class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

class CategoryAPIView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# @api_view(['GET'])
# def get_product(request):
#     """
#         get all product
#     """
#     product = Product.objects.all()
#     serializer = ProductSerializer(product, many=True)
#     return Response(serializer.data)    

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def post_product(request):
#     """
#         post product
#     """
#     serialiozer = ProductSerializer(data=request.data)
#     serialiozer.is_valid(raise_exception=True)
#     serialiozer.save(owner=request.user)
#     return Response(serialiozer.data, status=status.HTTP_201_CREATED)


# class ProductListGenericView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

# class ProductCreateGenericView(generics.CreateAPIView):
#     serializer_class = ProductSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)

# class ProductListCreateGenericView(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)

# class ProductAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self,request):
#         product = Product.objects.all()
#         serializer = ProductSerializer(product, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serialiozer = ProductSerializer(data=request.data)
#         serialiozer.is_valid(raise_exception=True)
#         serialiozer.save(owner=request.user)
#         return Response(serialiozer.data, status=status.HTTP_201_CREATED)


# class ProductViewSet(viewsets.ViewSet):
#     def list(self, request): # get
#         product = Product.objects.all()
#         serializer = ProductSerializer(product, many=True)
#         return Response(serializer.data)

#     def create(self, request): # post
#         serialiozer = ProductSerializer(data=request.data)
#         serialiozer.is_valid(raise_exception=True)
#         serialiozer.save(owner=request.user)
#         return Response(serialiozer.data, status=status.HTTP_201_CREATED)

# @api_view(['GET'])
# def get_hello(request):
#     big_func.delay()
#     return Response('get hello')
