from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext as _






class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(default='',null=True, max_length=255)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    phone_number = PhoneNumberField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    # img_profil = models.ImageField(default="default_profil.png")
    groups = models.ManyToManyField(
    Group,
    verbose_name=_('groups'),
    blank=True,
    help_text=_(
        'The groups this user belongs to. A user will get all permissions '
        'granted to each of their groups.'
    ),
    related_name='cybersec_users',  # Add related_name to resolve the clash
    related_query_name='cybersec_user'
)
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='cybersec_users_permissions',  # Add related_name to resolve the clash
        related_query_name='cybersec_user_permission',
        
    )





class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_name = models.CharField(null=False,max_length=255)
    ip_address = models.TextField(default='', null=True, max_length=50)
    device_type = models.CharField(null=False, max_length=50)
    operating_system = models.CharField(null=False, max_length=50)
    port_info = models.TextField(null=True, max_length=10)
    auth_credintials = models.TextField(null=True, max_length=255)
    scan_preferces = models.TextField(null=True, max_length=255)
    scan_schudule = models.TextField(null=True, max_length=255)

    def __str__(self):
        return self.device_name
