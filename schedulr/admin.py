from django.contrib import admin
from .models import Company, Position, Shift

# Register your models here.

admin.site.register(Position)
admin.site.register(Company)
admin.site.register(Shift)