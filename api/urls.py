from django.urls import path
from . import views

urlpatterns = [
    # path('products/', views.product_list),
    path("products/", views.ProductListApiView.as_view()),
    path("products/info/", views.ProductInfoApiView.as_view()),
    # path("products/<int:pk>/", views.product_detail),
    path("products/<int:pk>/", views.ProductDetailApiView.as_view()),
    # path("orders/", views.order_list),
    path("orders/", views.UserOrderListApiView.as_view()),
]
