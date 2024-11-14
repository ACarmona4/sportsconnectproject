from django.core.management.base import BaseCommand
from reservation.models import Availability, WaitList
from facility.models import Facilities
from datetime import time, timedelta, datetime
from django.core.mail import send_mail
from django.utils import timezone

class Command(BaseCommand):
    help = 'Assign time slots to existing Availability entries and notify waitlisted users'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        future_date = today + timedelta(days=7)  # Assumption of 7 days ahead scheduling
        facilities = Facilities.objects.all()

        for facility in facilities:
            availabilities = Availability.objects.filter(facilities=facility, date=future_date)

            # Verificar si los horarios ya existen para evitar duplicados
            existing_slots = set(availabilities.values_list('time_slot', flat=True))

            start_hour = 5
            end_hour = 21  # 9 PM in 24-hour format

            # Crear los horarios faltantes
            for hour in range(start_hour, end_hour + 1):
                time_slot = time(hour=hour)
                if time_slot not in existing_slots:
                    Availability.objects.create(
                        facilities=facility,
                        date=future_date,
                        time_slot=time_slot
                    )

            # After generating availability, check and notify waitlisted users
            waitlist_entries = WaitList.objects.filter(facilities=facility, date=future_date)
            for entry in waitlist_entries:
                # Send email notification
                send_mail(
                    'Horarios Disponibles',
                    f'Los horarios para {facility.name} el {future_date} están ahora disponibles. Puedes hacer tu reserva.',
                    'from@example.com',
                    [entry.user.email],
                    fail_silently=False,
                )
                # Optionally delete the entry if you don't need it anymore
                entry.delete()

        self.stdout.write(self.style.SUCCESS('Successfully assigned time slots and notified waitlisted users.'))
