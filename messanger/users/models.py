from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    # default required field: username, password,
    # optional fields: first name, last name, email
    # MtM relationships: permissions, groups
    # booleans: is_staff, is_active, is_superuser
    # other: last_active, date_joined
    pass # no custom fields yet

    def __str__(self):
        return self.username
