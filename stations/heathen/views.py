from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from heathen.models import Location, Member
from heathen.forms import HeathenForm


def members(request):
    locations = Location.objects.all()
    member_count = Member.objects.count()
    return render(
        request,
        'locations.html',
        {'locations': locations, 'total': member_count}
    )


def add_member(request, id):
    location = get_object_or_404(Location, pk=id)
    if request.method == 'POST':
        form = HeathenForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.location = location
            obj.save()
            messages.info(request, 'You have been registered successfully')
            return redirect('locations')
    else:
        form = HeathenForm()
    return render(
        request,
        'add_member.html',
        {'location': location, 'form': form}
    )
