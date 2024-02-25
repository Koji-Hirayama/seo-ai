from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('ai_products.urls')),
    path('authen/', include('djoser.urls.jwt')), # token獲得用
]
