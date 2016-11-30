
from django.core.management.base import NoneCommand
from django.utils import timezone

from core.models import Tournament


class Command(NoneCommand):
    help = "Starts/ends tournament and created next stages"

    def handle(self, *args, **options):
        for t in Tournament.objects.filter(
            started_at__isnull=True,
            start_at__gte=timezone.now().date(),
        ):
            t.start()

        for t in Tournament.objects.filter(
            started_at__isnull=False,
            ended_at__isnull=True,
        ):
            active_stage = t.get_active_stage()
            if active_stage and active_stage.deadline >= timezone.now():
                t.create_next_stage()
