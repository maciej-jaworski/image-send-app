from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users import models


class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "is_active",
    )
    list_filter = (
        "is_superuser",
        "is_active",
        "groups",
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                    "groups",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    def has_change_permission(self, request, obj=None):
        # Only superusers can edit other superusers
        if obj and obj.is_superuser:
            return request.user.is_superuser

        return super().has_change_permission(request, obj=obj)


admin.site.register(models.User, CustomUserAdmin)
