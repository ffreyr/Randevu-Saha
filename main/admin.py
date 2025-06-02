from django.contrib import admin
from .models import CustomUser, Halisaha, Reservation
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type', 'favorite_sahalar')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_type', 'favorite_sahalar')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Halisaha)
admin.site.register(Reservation)

