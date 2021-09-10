from django.contrib import admin

from .models import MPs, MP_post, PostImages
# Register your models here.

@admin.register(MPs)
class MPsAdmin(admin.ModelAdmin):
	pass

@admin.register(MP_post)
class MP_postAdmin(admin.ModelAdmin):
	pass

@admin.register(PostImages)
class PostImagesAdmin(admin.ModelAdmin):
	pass