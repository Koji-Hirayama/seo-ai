from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from ai_products.domain.user import User as DomainUser

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('email is must')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using= self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
    
    @classmethod
    def from_domain(cls, obj: DomainUser) -> "User":
        """ドメインモデルからのファクトリメソッド"""
        return cls(id=obj.id, name=obj.name)

    def to_domain(self) -> DomainUser:
        """Djangoモデルからドメインモデルに変換するメソッド"""
        return DomainUser(
            id=self.id,
            email=self.email,
            is_active=self.is_active,
            is_staff=self.is_staff,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
    