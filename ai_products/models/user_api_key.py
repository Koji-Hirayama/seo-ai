from django.db import models
from ai_products.models.user import User
from .api_provider import ApiProvider

class UserApikey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="apikeys")
    api_provider = models.ForeignKey(ApiProvider, on_delete=models.CASCADE, related_name="apikeys")
    key = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    