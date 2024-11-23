from django.contrib import admin
from .models import image_model,classes, Response

admin.site.register(image_model)
admin.site.register(classes)
admin.site.register(Response)
# Register your models here.
