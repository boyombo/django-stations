from django.core.management.base import BaseCommand
from medic.models import Candidate, Subscriber, BloodRequest, is_compatible


class Command(BaseCommand):
    help = "Creates candidates compatible with a blood request"

    def handle(self, *args, **kwargs):
        count = 0
        for rqst in BloodRequest.objects.filter(processed=False):
            subscribers = Subscriber.objects.filter(location=rqst.location)
            for sub in subscribers:
                if is_compatible(sub.blood_type.name, rqst.blood_type.name):
                    Candidate.objects.create(
                        blood_request=rqst,
                        subscriber=sub,
                        active=True)
                    count += 1
            rqst.processed = True
            rqst.save()
        self.stdout.write(
            self.style.SUCCESS('Created {} candidates'.format(count)))
