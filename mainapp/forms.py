from django.forms import ModelForm
from mainapp.models import AttendanceRecord, User


class AddUserForm(ModelForm):

    class Meta:
        model = User
        exclude = ['status']
