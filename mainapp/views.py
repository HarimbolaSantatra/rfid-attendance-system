from django.shortcuts import render, redirect
from mainapp.models import AttendanceRecord, User
from .forms import AddUserForm, DeleteUserForm, UpdateUserForm  # forms
from django.contrib.auth import authenticate, login, logout  # user login and logout

# for flash messages
from django.contrib import messages

# We put decorator on every view that we want to be restricted when the user is logged out
from django.contrib.auth.decorators import login_required


def login_page(request):
    # Atao login_page satria login efa method Django

    if request.user.is_authenticated:  # If already logged in, login page in not available anymore
        return redirect('homepage')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Login successfully !')
                return redirect('homepage')
            else:
                messages.error(request, 'Username or password incorrect !')

        context = {}
        return render(request, 'login.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
# View: index page
def homepage(request):

    context = {
    }
    return render(request, 'index.html', context)


@login_required(login_url='login')
def add_user(request):
    form = AddUserForm()
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():

            # Set default field for the new user
            new_user = form.save(commit=False)
            new_user.status = 'a'

            new_user.save()
            return redirect('users')
    context = {'form': form}
    return render(request, 'add_user.html', context)


@login_required(login_url='login')
def update_user(request, pk):

    # Extract user
    user = User.objects.get(id=pk)

    # Set initial value of the form
    form = UpdateUserForm(instance=user)

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')

    context = {'form': form, 'user':user}
    return render(request, 'update_user.html', context)


@login_required(login_url='login')
def delete_user(request, pk):

    # Extract user
    user = User.objects.get(id=pk)

    if request.method == 'POST':
        user.delete()
        return redirect('users')

    return render(request, 'delete_user.html', {'user':user})


@login_required(login_url='login')
def user_page(request, pk):

    # Extract user
    user = User.objects.get(id=pk)

    # Set initial value of the form
    form = DeleteUserForm(instance=user)

    if request.method == 'POST':
        form = DeleteUserForm(request.POST, instance=user)
        if form.is_valid():
            form.delete()
    context = {'user':user}
    return render(request, 'user_page.html', context)


@login_required(login_url='login')
# View: today's attendance page
def today(request):
    # attendance_instances_enum return an enumerated object
    # We use it to have a new ID. It's not for the core database, just for display. View, not controller
    today_attendance_instances_enum = enumerate(AttendanceRecord.custom_manager.get_today().order_by('-date'), 1)

    context = {
        'today_attendance_instances_enum': today_attendance_instances_enum,
    }
    return render(request, 'today.html', context=context)


@login_required(login_url='login')
def accepted_user(request):
    accepted_user_list = User.objects.filter(status='a')
    accepted_user_number = accepted_user_list.count()
    context = {
        'accepted_user_number': accepted_user_number,
        'accepted_user_list': accepted_user_list,
    }
    return render(request, 'accepted_user.html', context=context)


@login_required(login_url='login')
def full(request):
    # attendance_instances_enum return an enumerated object
    # We use it to have a new ID. It's not for the core database, just for display. View, not controller
    attendance_instances_enum = enumerate(AttendanceRecord.objects.all().order_by('-date'), 1)

    context = {
        'attendance_instances_enum': attendance_instances_enum,
    }
    return render(request, 'full.html', context=context)

