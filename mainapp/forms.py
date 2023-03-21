from django import forms
from django.forms import ModelForm
from mainapp.models import AttendanceRecord, User


class AddUserForm(ModelForm):

    class Meta:
        model = User
        exclude = ['status']
        

class UpdateUserForm(ModelForm):

    class Meta:
        model = User
        exclude = ['status']

class DeleteUserForm(ModelForm):

    class Meta:
        model = User
        fields = '__all__'
        