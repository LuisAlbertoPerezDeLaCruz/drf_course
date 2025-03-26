from django.contrib import admin
from django.urls import path
from api.urls import urlpatterns as api_urls

urlpatterns = [
    path("admin/", admin.site.urls),  # Include the API URLs
] + api_urls
