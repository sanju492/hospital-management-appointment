from django.contrib import admin

from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'age',
        'gender',
        'created_at',
    )

    list_filter = (
        'gender',
        'created_at',
    )

    search_fields = (
        'user__username',
        'user__email',
        'user__first_name',
    )