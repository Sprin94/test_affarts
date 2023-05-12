from django.core.management.base import BaseCommand
from django.db.models import Count, Q
from people.models import Person


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='Person ID')

    def handle(self, *args, **options):
        d = (Person.objects.annotate(
            positive=Count('actions', filter=Q(actions__rating__gt=5)),
            negative=Count('actions', filter=Q(actions__rating__lt=5)),
            neutral=Count('actions', filter=Q(actions__rating=5)),
        ).values(
            'name', 'surname', 'positive', 'negative', 'neutral'
        ).get(pk=options['id']))
        print(d)
