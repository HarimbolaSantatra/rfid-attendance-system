from django.shortcuts import render
from mainapp.models import AttendanceRecord, User
from .forms import AddUserForm
from django.contrib.auth import authenticate, login, logout


def login(request):
    if request.method == 'POST':
        request.POST.get('username')
        request.POST.get('password')
    context = {}
    return render(request, 'login.html', context)


# View: index page
def homepage(request):

    context = {
    }
    return render(request, 'index.html', context)


def add_user(request):
    form = AddUserForm()
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'add_user.html', context)


# View: today's attendance page
def today(request):
    # attendance_instances_enum return an enumerated object
    # We use it to have a new ID. It's not for the core database, just for display. View, not controller
    today_attendance_instances_enum = enumerate(AttendanceRecord.custom_manager.get_today().order_by('-date'), 1)

    context = {
        'today_attendance_instances_enum': today_attendance_instances_enum,
    }
    return render(request, 'today.html', context=context)


def accepted_user(request):
    accepted_user_list = User.objects.filter(status='a')
    accepted_user_number = accepted_user_list.count()
    context = {
        'accepted_user_number': accepted_user_number,
        'accepted_user_list': accepted_user_list,
    }
    return render(request, 'accepted_user.html', context=context)


def full(request):
    # attendance_instances_enum return an enumerated object
    # We use it to have a new ID. It's not for the core database, just for display. View, not controller
    attendance_instances_enum = enumerate(AttendanceRecord.objects.all().order_by('-date'), 1)

    context = {
        'attendance_instances_enum': attendance_instances_enum,
    }
    return render(request, 'full.html', context=context)

