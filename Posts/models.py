from django.db import models
import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your models here.



class PostImages(models.Model):
	image_url = models.URLField(max_length=500, null=True, blank=True)
	image_name = models.CharField(max_length=200, null=True, blank=True)
	uploadedImage = models.ImageField(upload_to='images/', blank=True, null=True)
	data = models.JSONField(null=True, blank=True)
	mp_id = models.IntegerField(null=True, blank=True)
	post_number = models.BigIntegerField(null=True, blank=True)

class MPs(models.Model):
	index = models.IntegerField(null=True)
	name = models.CharField(max_length = 100)
	party = models.CharField(max_length = 100)
	fb_identifier = models.CharField(max_length = 200)
	constituency = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return self.name

class MP_post(models.Model):
	post_number = models.BigIntegerField(blank=True, null=True)
	post_text = models.TextField(blank=True, null=True)
	post_time = models.DateTimeField(blank=True, null=True)
	post_image = models.ManyToManyField(PostImages, blank=True)
	post_likes = models.IntegerField(blank=True, null=True)
	post_url = models.TextField(blank=True, null=True)
	# post_loves = models.IntegerField(blank=True, null=True)
	# post_wow = models.IntegerField(blank=True, null=True)
	# post_cares = models.IntegerField(blank=True, null=True)
	# post_sad = models.IntegerField(blank=True, null=True)
	# post_angry = models.IntegerField(blank=True, null=True)
	# post_haha = models.IntegerField(blank=True, null=True)
	post_shares = models.IntegerField(blank=True, null=True)
	post_video = models.TextField(blank=True, null=True)
	post_comment = models.IntegerField(blank=True, null=True)
	# post_reaction_count = models.IntegerField(blank=True, null=True)
	mp = models.ForeignKey(MPs, on_delete=models.CASCADE)

	def __str__(self):
		return self.mp.name
