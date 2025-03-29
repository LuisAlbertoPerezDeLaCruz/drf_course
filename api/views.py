from django.db.models import Max
from django.shortcuts import get_object_or_404
from api.serializers import (
    ProductSerializerGet,
    OrderSerializer,
    ProductInfoSerializer,
    ProductSerializerPost,
)
from api.models import Product, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView

# @api_view(["GET"])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)


class ProductListApiView(generics.ListAPIView):
    queryset = Product.objects.exclude(stock=0)  # Exclude products with stock = 0
    serializer_class = ProductSerializerGet


class ProductCreateApiView(generics.CreateAPIView):
    model = Product
    serializer_class = ProductSerializerPost

    def create(
        self, request, *args, **kwargs
    ):  # Override the create method to add custom behavior
        print(request.data)  # Debugging line to check incoming data
        return super().create(request, *args, **kwargs)


class ProductCreateListApiView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializerGet

    def get_permissions(self):
        self.permission_classes = [AllowAny]  # Default permission for GET requests
        if self.request.method == "POST":
            # If the request method is POST, require admin permissions
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


# @api_view(["GET"])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)


# class ProductDetailApiView(generics.RetrieveAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializerGet


class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializerGet

    def get_permissions(self):
        self.permission_classes = [AllowAny]  # Default permission for GET requests
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            # If the request method is POST, require admin permissions
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


# @api_view(["GET"])
# def order_list(request):
#     orders = Order.objects.prefetch_related("items__product")
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)


class UserOrderListApiView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(user=user)


# @api_view(["GET"])
# def product_info(request):
#     products = Product.objects.all()
#     serializer = ProductInfoSerializer(
#         {
#             "products": products,
#             "count": len(products),
#             "max_price": products.aggregate(max_price=Max("price"))["max_price"],
#         }
#     )
#     return Response(serializer.data)


class ProductInfoApiView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer(
            {
                "products": products,
                "count": len(products),
                "max_price": products.aggregate(max_price=Max("price"))["max_price"],
            }
        )
        return Response(serializer.data)
