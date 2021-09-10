from Posts.models import MPs, MP_post, PostImages
from django.core.management import BaseCommand
from PIL import Image
import requests


import io
import os

from google.cloud import vision


class Command(BaseCommand):
	def handle(self, *args, **options):


		os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="fluted-layout-316721-5fe800e09e0b.json"

		client = vision.ImageAnnotatorClient()


		def classify(img_location):



			classifications = {}
			with io.open(img_location, 'rb') as image_file:
				content = image_file.read()

			image = vision.Image(content=content)

			# Performs label detection on the image file
			response = client.label_detection(image=image)
			labels = response.label_annotations

			for label in labels:
				classifications[label.description] = label.score


			return classifications

		print(classify('media/images/pngimage.png'))