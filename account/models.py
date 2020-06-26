from django.db import models
from django.contrib.auth.models import Group

# Create your models here.
# Added status field in Existing Group Model
Group.add_to_class('status', models.BooleanField(default=True))
