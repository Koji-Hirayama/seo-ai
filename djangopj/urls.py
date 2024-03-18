from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("ai_products.urls")),
    # Swagger関係
    # ! 本番環境では、公開しないように設定する。(リリース時対応)
    # ================================
    # アクセスするとテキストファイルをダウンロードできます
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # SwaggerUIの設定
    # アクセスするとSwaggerUIが表示されるよう設定します
    path(
        "api/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # Redocの設定
    # アクセスするとRedocが表示されるよう設定します
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # ================================
]
