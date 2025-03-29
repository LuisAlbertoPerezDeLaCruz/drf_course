from django.contrib import admin
from django.urls import include, path
from api.urls import urlpatterns as api_urls
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),  # Include the API URLs
    path("", include("api.urls")),  # Include the API URLs from the api app
    path(
        "silk/", include("silk.urls", namespace="silk")
    ),  # Include Silk URLs for profiling
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
