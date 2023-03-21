from django.contrib import admin
from .models import User, AttendanceRecord


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date')
    list_filter = ('date', 'user')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'card_id', 'status')
