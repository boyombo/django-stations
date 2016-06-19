from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from booking.forms import ResidentForm
from booking.models import Resident


@login_required
def dashboard(request):
    estate = request.user.estate
    residents = Resident.objects.filter(estate=estate)
    if request.method == 'POST':
        form = ResidentForm(request.POST)
        if form.is_valid():
            resident = form.save(commit=False)
            resident.estate = request.user.estate
            resident.active = False
            resident.save()
            return redirect('dashboard')
    else:
        form = ResidentForm()
    return render(request, 'booking/dashboard.html',
                  {'residents': residents, 'sms_credit': 0, 'form': form})


def remove(request, id):
    resident = get_object_or_404(Resident, pk=id)
    resident.delete()
    return redirect('dashboard')
