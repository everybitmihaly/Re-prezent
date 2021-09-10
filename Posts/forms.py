from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Button, HTML
from crispy_forms.bootstrap import InlineCheckboxes, FieldWithButtons


from django.db import models
from .models import MPs

PARTIES = [('Fidesz', 'Fidesz'),
	('DK', 'DK'),
	('Párbeszéd', 'Párbeszéd'),
	('Jobbik', 'Jobbik'),
	('Együtt', 'Együtt'),
	('LMP', 'LMP'),
	('MSZP', 'MSZP'),
	('MNÖ', 'MNÖ'),
	('független', 'független'),
	('Volner Party', 'Volner Party')]

MP_NAMES_LIST = list(MPs.objects.values_list('name', flat=True))
MP_NAMES = [(mp, mp) for mp in MP_NAMES_LIST]

class PostSearchForm(forms.Form):
	search_text = forms.CharField(max_length=50,
		widget=forms.TextInput(attrs={'placeholder': 'Search for any text in all posts...'})
		)
	def __init__(self, *args, **kwargs):
		super(PostSearchForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_show_labels = False 
		self.helper.layout = Layout(
			FieldWithButtons(
				Field('search_text', autofocus='autofocus'),
				Submit('', ('Search'), css_class='btn-light')
			)
		)

class ChartForm(forms.Form):
	parties = forms.MultipleChoiceField(required=False, label='Party choice', 
		choices=PARTIES,
		widget=forms.CheckboxSelectMultiple())

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-graphform'
		self.helper.form_class = 'blueForms'
		self.helper.form_method = 'post'
		self.helper.form_action = 'submit_survey'
		self.helper.layout = Layout(
			InlineCheckboxes('parties')

			)

		self.helper.add_input(Submit('submit', 'Submit'))


class GraphForm(forms.Form):
	#name = forms.MultipleChoiceField(required=False, label='MP', choices=MP_NAMES)
	parties = forms.MultipleChoiceField(required=False, label='Party choice', 
		choices=PARTIES,
		widget=forms.CheckboxSelectMultiple())

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-graphform'
		self.helper.form_class = 'blueForms'
		self.helper.form_method = 'post'
		self.helper.form_action = 'submit_survey'
		self.helper.layout = Layout(
			InlineCheckboxes('parties')

			)

		self.helper.add_input(Submit('submit', 'Submit'))


class ImageForm(forms.Form):
	image_to_search = forms.CharField(max_length=50,
		widget=forms.TextInput(attrs={'placeholder': 'Search for image keyword e.g.: car, house, ice cream, food...'})
		)
	parties = forms.MultipleChoiceField(required=False, 
		choices=PARTIES,
		widget=forms.CheckboxSelectMultiple())
	def __init__(self, *args, **kwargs):
		super(ImageForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_show_labels = False 
		self.helper.layout = Layout(
			HTML("<div style='width: 655px; margin: auto;'>"),
			InlineCheckboxes('parties', css_class="inline"),
			HTML("</div>"),
			HTML("<br>"),
			FieldWithButtons(
				Field('image_to_search', autofocus='autofocus'),
				Submit('', ('Search'), css_class='btn-light')
			)
		)

