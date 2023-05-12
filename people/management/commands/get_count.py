from django.core.management.base import BaseCommand
from django.db.models import Avg, Q
from people.models import Person


class Command(BaseCommand):
    def handle(self, *args, **options):
        d = Person.objects.annotate(
            avg_rating=Avg('actions__rating')
        ).filter(
            Q(is_workless__isnull=True) & Q(residence__city='N')
        ).filter(
            (Q(marriage_1__finish__isnull=True) | Q(marriage_2__finish__isnull=True)) &
            (Q(marriage_1__start__isnull=False) | Q(marriage_2__start__isnull=False)) &
            Q(avg_rating__gt=6)
        ).all()
        print(d)
