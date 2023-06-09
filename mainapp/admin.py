from django.contrib import admin
from .models import UploadedMovie, MergedMovie, ShortLink

# Register your models here.

admin.site.register(UploadedMovie)
admin.site.register(MergedMovie)
admin.site.register(ShortLink)
