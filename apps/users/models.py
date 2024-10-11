from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    role_id = models.PositiveIntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    # language = models.ForeignKey('Language', models.DO_NOTHING)  # Make sure Language is defined

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        managed = False
        db_table = 'user'

    def has_perm(self, perm, obj=None) -> bool:
        """
        Check if the user has the specified permission.
        """
        # If the user is a superuser, they automatically have all permissions
        if self.is_superuser:
            return True

        # Otherwise, check the specific permission
        return self.user_permissions.filter(codename=perm).exists() or self.groups.filter(
            permissions__codename=perm).exists()

    def has_module_perms(self, app_label) -> bool:
        """
        Check if the user has any permissions for the specified app/module.
        """
        # Superusers have all permissions
        if self.is_superuser:
            return True
        # Check if the user has any permissions for the app
        return super().has_module_perms(app_label)

# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     objects: UserManager = UserManager()
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#
#     def __str__(self):
#         return self.email
#
#     def has_perm(self, perm, obj=None) -> bool:
#         """
#         Check if the user has the specified permission.
#         """
#         # If the user is a superuser, they automatically have all permissions
#         if self.is_superuser:
#             return True
#
#         # Otherwise, check the specific permission
#         return self.user_permissions.filter(codename=perm).exists() or self.groups.filter(permissions__codename=perm).exists()
#
#     def has_module_perms(self, app_label) -> bool:
#         """
#         Check if the user has any permissions for the specified app/module.
#         """
#         # Superusers have all permissions
#         if self.is_superuser:
#             return True
#         # Check if the user has any permissions for the app
#         return super().has_module_perms(app_label)

