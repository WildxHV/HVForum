from django.contrib import admin

# Register your models here.
from .models import Discussions, Comments

admin.site.register(Discussions)
admin.site.register(Comments)