from csv import DictReader

from django.core.management import BaseCommand

from Posts.models import MPs

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the pet data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from test_list_extra.csv into our MPs model"

    def handle(self, *args, **options):
        # if MPs.objects.exists():
        #     print('MP data already loaded...exiting.')
        #     print(ALREDY_LOADED_ERROR_MESSAGE)
        #     return

        print("Loading MP data for MPs available")
        for row in DictReader(open('./test_list3.csv')):
            MP = MPs()
            MP.index = row['index']
            MP.name = row['name']
            MP.party = row['party']
            MP.fb_identifier = row['fb_id']
            MP.save()
