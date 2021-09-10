from Posts.models import MPs, MP_post, PostImages
from django.core.management import BaseCommand
from facebook_scraper import get_posts
from PIL import Image
import requests
import time
import random

import io
import os

from google.cloud import vision



class Command(BaseCommand):
	def handle(self, *args, **options):

		os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="fluted-layout-316721-5fe800e09e0b.json"

		client = vision.ImageAnnotatorClient()


		def resizer(w, h):
			while w > 400:
				w = w/2
				h = h/2
			return int(w), int(h)

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
	
		all_MPs_fb_id = list(MPs.objects.values_list('fb_identifier', flat=True))
		random.shuffle(all_MPs_fb_id)
		print(all_MPs_fb_id)
		for fb_id in all_MPs_fb_id:

			print(fb_id)
			print('Index of MP:', all_MPs_fb_id.index(fb_id))
			for post in get_posts(fb_id, pages=5, timeout=60, extra_info=True, cookies='Posts/management/commands/cookies.json'):

				num_results = MP_post.objects.all().filter(post_number=post['post_id']).count()

				if num_results == 0:
					# collect data needed to be saved

					post_number = post['post_id']
					post_text = post['post_text']
					post_time = post['time']
					#post_reaction_count = mp_data[post]['reaction_count']
					post_likes = post['likes']
					#post_loves = mp_data[post]['reactions']['loves']
					#post_wow = mp_data[post]['reactions']['wow']
					#post_cares = mp_data[post]['reactions']['cares']
					#post_sad = mp_data[post]['reactions']['sad']
					#post_angry = mp_data[post]['reactions']['angry']
					#post_haha = mp_data[post]['reactions']['haha']
					post_video = post['video']
					post_comment = post['comments']
					post_shares = post['shares']
					post_url = post['post_url']
					#post_image = mp_data[post]['image']

					author = MPs.objects.get(fb_identifier=fb_id)

					new_post = MP_post(post_number=post_number, post_text=post_text, post_time=post_time,
					post_likes=post_likes, post_video=post_video, post_comment=post_comment,
					post_url=post_url, post_shares=post_shares, mp=author)
					new_post.save()
					counter = 0

					try:
						print(len(post["images"]))


						for image in post['images']:

							try:
								im = Image.open(requests.get(image, stream=True).raw)
							except:
								print("couldn't request image")
							new_w, new_h = resizer(im.size[0], im.size[1])
							im = im.resize((new_w, new_h))
							save_name = str(post["post_id"]) + '_' + str(counter)
							im.save(f'media/images/{save_name}.png')
							print('intermediate file saved')

							data_dict = classify(f'media/images/{save_name}.png')
							print('image saved')
							image_to_save = PostImages(image_url=image, image_name=save_name, uploadedImage=f'images/{save_name}.png', data=data_dict, post_number=post["post_id"], mp_id=author.id)
							image_to_save.save()
							print(data_dict)

							

			
							new_post.post_image.add(image_to_save)


							counter += 1

							new_post.save()
					except:
						print('no image')

				if num_results == 1:
					p_to_update = MP_post.objects.get(post_number=post['post_id'])
					p_to_update.post_likes = post['likes']
					p_to_update.post_comment = post['comments']
					p_to_update.post_shares = post['shares']
					p_to_update.save()
					print('Updated', post['post_id'])
#					print('next')
