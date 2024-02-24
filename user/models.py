from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# utils
import uuid 


class RegisterUser(AbstractUser):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, unique=True)
