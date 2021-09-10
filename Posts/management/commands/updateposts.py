from csv import DictReader

from django.core.management import BaseCommand

from Posts.models import MPs, MP_post, PostImages

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the pet data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from test_list_extra.csv into our MPs model"

    def handle(self, *args, **options):

        all_posts = MP_post.objects.all()

        for post in all_posts:

            for image in post.post_image.all():

                if image.post_number:
                    continue
                else:
                    image.post_number = post.post_number
                    image.save()
                    print(image.post_number)
                
                if image.mp_id:
                    continue
                else:
                    image.mp_id = post.mp.id
                    image.save()
                    print(image.mp_id)

