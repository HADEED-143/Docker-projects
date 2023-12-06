from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Import your custom user model

class CustomUserAdmin(UserAdmin):
    model = CustomUser  # Use your custom user model
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'role')  # Specify the fields you want to display in the user list
    list_filter = ('is_staff', 'role')  # Add filters for user list
    search_fields = ('email', 'first_name', 'last_name')  # Add search functionality for user list
    ordering = ('email',)  # Define the default sorting order

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'age', 'gender', 'role', 'profile_picture', 'city', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

# Register your custom user admin class with the admin site
admin.site.register(CustomUser, CustomUserAdmin)
