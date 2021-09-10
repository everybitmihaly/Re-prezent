from __future__ import unicode_literals, division

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView
from .models import MPs, MP_post, PostImages
from collections import Counter
from operator import itemgetter
import string
from .forms import ChartForm, GraphForm, ImageForm, PostSearchForm
from PIL import Image
import requests
import operator

from django.conf import settings

def home(request):


	animalPics = PostImages.objects.filter(
		data__has_any_keys=['dog', 'Dog', 'cat', 'Cat', 'horse', 'Horse', 'bird', 'Bird', 'cow', 'Cow']
		)

	ids = []
	for im in animalPics:
		ids.append(im.id)

	posts = MP_post.objects.all().filter(post_image__in=ids)

	to_pass = {}

	for x in ids:
		try:

			imPass = PostImages.objects.get(id=x)
			postPass = MP_post.objects.get(post_image__id=x)
			#to_pass.append((postPass, imPass))
			to_pass[postPass] = imPass
		except:
			continue


	context = {'post_dict': to_pass}


	return render(request, 'Posts/home.html', context=context)

class MPListView(ListView):
	model = MPs
	template_name = 'Posts/mplist.html'
	context_object_name = 'mps'

def ImagesView(request):
	form = ImageForm(request.POST)
	if request.method == 'POST':

		if form.is_valid():
			# image_to_search is the query word

			parties = form.cleaned_data['parties']

			if len(parties) == 0:
				parties = ['Fidesz', 'DK', 'Párbeszéd', 'Jobbik', 'Együtt', 'LMP', 'MSZP', 'MNÖ', 'Volner Party', 'független']
			query = form.cleaned_data['image_to_search']
			query_capital = query.capitalize()


			mps = MPs.objects.all().filter(party__in=parties)
			# posts of MPs from select parties
			party_posts = MP_post.objects.all().filter(mp__in=mps)

			# get ids of select party images
			image_ids = []
			for post in party_posts:
				for image in post.post_image.all():
					image_ids.append(image.id)


			# Filter select party images with query
			queryset = PostImages.objects.filter(
				Q(id__in=image_ids),
				Q(data__has_key=query) | Q(data__has_key=query_capital)
				)

			# create list of image object IDs
			ids = []
			for im in queryset:
				ids.append(im.id)

			# create dict to pass
			to_pass = {}

			# for each image, create entry in dict to pass with post as key and image as value
			for x in ids:
				try:
					image = PostImages.objects.get(id=x)
					post = MP_post.objects.get(post_image__id=x)
					to_pass[post] = image
				except:
					continue

			to_pass2 = {}

			for i in (sorted(to_pass.keys(), key=operator.attrgetter('post_time'), reverse=True)):
				to_pass2[i] = to_pass[i]

			context = {'form':form, 'to_pass':to_pass2}
	else:

		images = PostImages.objects.all()
		all_keys = []
		for image in images:
			for key, value in image.data.items():
				all_keys.append(key)

		keys = Counter(all_keys).keys()
		counter = Counter(all_keys).values()
		key_counter = {}

		for i in zip(keys, counter):
			key_counter[i[0]] = i[1]

		a2 = sorted(key_counter.items(), key=lambda x: x[1], reverse=True)
		context = {'form':form, 'search': 'search', 'key_counter': a2}

	return render(request, 'Posts/image_search.html', context=context)


def ImageSearchResultsView(request):
	if request.method == "GET":
		query = request.GET.get('q')
		queryset = PostImages.objects.all().filter(data__has_key=query)
		print(queryset)

		# create list of image object IDs
		ids = []
		for im in queryset:
			ids.append(im.id)

		# for each image, create entry in dict to pass with post as key and image as value
		to_pass = {}
		for x in ids:
			try:
				image = PostImages.objects.get(id=x)
				post = MP_post.objects.get(post_image__id=x)
				to_pass[post] = image
			except:
				continue

		to_pass2 = {}

		for i in (sorted(to_pass.keys(), key=operator.attrgetter('post_time'), reverse=True)):
			to_pass2[i] = to_pass[i]

		context = {'page_title': query, 'to_pass':to_pass2}

	else:
		query = 'No search was given'
		context = {'page_title': query}

	return render(request, 'Posts/image_search_results.html', context=context)



def mplist(request):

	form = ChartForm(request.POST)
	if request.method == 'POST':
		

		if form.is_valid():
			parties = form.cleaned_data['parties']

		#result_posts = MP_post.objects.all().filter(mp__party=party)
		mps = MPs.objects.all().filter(party__in=parties)

		
	else:
		mps = MPs.objects.all()
	return render(request, 'Posts/mplist.html', {'form':form, 'mps': mps,})

def posts(request):
	# all_posts = MP_post.objects.all().order_by('-post_time')

	# paginator = Paginator(all_posts, 50)

	# page_number = request.GET.get('page')

	# page_obj = paginator.get_page(page_number)

	# return render(request, 'Posts/posts.html', {'all_posts': all_posts})
    


	form = PostSearchForm(request.POST)
	if request.method == 'POST':

		if form.is_valid():
			query = form.cleaned_data['search_text']

			all_posts=MP_post.objects.filter(post_text__icontains=query).order_by('-post_time')

			context = {'all_posts': all_posts, 'form': form, 'query':query}
		



	else:

		all_posts = MP_post.objects.all()

		post_counter = len(all_posts)

		context = {'post_counter': post_counter, 'form': form}

	return render(request, 'Posts/posts.html', context=context)

def search(request):
	query=None
	results=[]
	if request.method=="GET":
		query=request.GET.get('search')
		results=MP_post.objects.filter(Q(post_text__icontains=query)).order_by('-post_time')
	print(type(results))
	return render(request, 'Posts/search.html', {'query': query,
										'results': results})

class MPPostListView(ListView):
	#queryset = MP_post.objects.order_by('-post_time')
	model = MP_post
	template_name = 'Posts/postofmp.html'
	context_object_name = 'posts'



	def get_queryset(self):
		MP = get_object_or_404(MPs, id=self.kwargs.get('id'))
		return MP_post.objects.filter(mp=MP).order_by('-post_time')



