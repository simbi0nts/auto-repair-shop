
import datetime

from django.shortcuts import render
from django.utils.timezone import get_current_timezone
from django.utils.translation import gettext_lazy as _

from core.models.workflow import Appointments


def home(request):
    context = {}

    appointment = {
        'exists': False,
        'info': None
    }

    if request.user.is_authenticated:
        appointment = Appointments.objects.filter(
            customer=request.user,
            date__gte=datetime.date.today()
        ).order_by('date').first()

        if appointment:
            _time = appointment.time.astimezone(get_current_timezone()).strftime('%H:%M')

            info = _("Date: {} \nTime: {} \nDuration: {} \nMechanic: {}").format(
                appointment.date, _time, appointment.duration, appointment.workman.get_full_name())

            appointment = {
                'exists': True,
                'info': info
            }

    context['appointment'] = appointment

    return render(request, 'core/home.html', context)
