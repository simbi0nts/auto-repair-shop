from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.forms import UserCreationForm, UserChangeForm
from core.models import (Appointments, AppointmentsArchive, RepairShop, User,
                         UserCar, Workman, WorkRegime, WorkRegimeDetail,
                         WorkRegimeExceptions)


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': ('password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = tuple()
    ordering = tuple()


admin.site.register(User, UserAdmin)

admin.site.register(RepairShop)
admin.site.register(Workman)
admin.site.register(UserCar)
admin.site.register(WorkRegime)
admin.site.register(WorkRegimeExceptions)
admin.site.register(WorkRegimeDetail)
admin.site.register(AppointmentsArchive)
admin.site.register(Appointments)
