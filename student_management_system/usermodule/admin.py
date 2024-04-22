from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from usermodule.models import CustomUser, Staff, Student, HOD, Courses, Semester
# Register your models here.

class UserModel(UserAdmin):
    list_display = ('username', 'user_type', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('user_type',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type', 'is_staff', 'is_active')}
        ),
    )

admin.site.register(CustomUser,UserModel)
admin.site.register(HOD)
admin.site.register(Staff)
admin.site.register(Student)
admin.site.register(Courses)
admin.site.register(Semester)
