from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser, StudentRecord
from django.contrib.auth.admin import UserAdmin
import re


# ✅ Custom form for StudentRecord validation in Admin
class StudentRecordAdminForm(forms.ModelForm):
    class Meta:
        model = StudentRecord
        fields = "__all__"

    def clean_lrn(self):
        lrn = self.cleaned_data.get("lrn", "")
        if not re.fullmatch(r"\d{12}", lrn):
            raise ValidationError("LRN must be exactly 12 digits.")
        return lrn

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name", "")
        if not re.fullmatch(r"[A-Za-z\s\-]+", last_name):
            raise ValidationError("Last name must contain only letters.")
        return last_name

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name", "")
        if not re.fullmatch(r"[A-Za-z\s\-]+", first_name):
            raise ValidationError("First name must contain only letters.")
        return first_name

    def clean_middle_name(self):
        middle_name = self.cleaned_data.get("middle_name", "")
        if middle_name and not re.fullmatch(r"[A-Za-z\s\-]+", middle_name):
            raise ValidationError("Middle name must contain only letters.")
        return middle_name


# ✅ Custom admin for CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("username", "email", "role")
    ordering = ("username",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("email",)}),
        ("Permissions", {"fields": ("role", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "role", "password1", "password2", "is_active", "is_staff"),
        }),
    )


# ✅ Custom admin for StudentRecord with validation
@admin.register(StudentRecord)
class StudentRecordAdmin(admin.ModelAdmin):
    form = StudentRecordAdminForm  # <-- Validation applied here!
    list_display = ("lrn", "last_name", "first_name", "middle_name")
    search_fields = ("lrn", "last_name", "first_name")
    list_filter = ("last_name",)
    ordering = ("last_name",)

    fieldsets = (
        ("Student Info", {
            "fields": ("lrn", "last_name", "first_name", "middle_name")
        }),
    )
