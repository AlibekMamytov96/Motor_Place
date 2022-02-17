from django.contrib import admin

# Register your models here.
from .models import *


class ImageInLine(admin.TabularInline):
    model = CarImage
    min_num = 1
    max_num = 5

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    inlines = [ImageInLine, ]


admin.site.register(Brand)
admin.site.register(Comment)
