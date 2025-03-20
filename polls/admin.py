from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Question, Choice, CustomUser


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("choice_text", "choice_question_text", "voters")
    filter_horizontal=("voter",)
    def choice_question_text(self, obj):
        return obj.question.question_text
    def voters(self, obj):
        return f"{obj.votes}(Voted by:{', '.join([user.email for user in obj.voter.all()])})"
    
    voters.short_description ="Votes & Voters"

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "full_name", "is_staff", "is_superuser", "is_active")
    search_fields = ("email", "full_name")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("full_name",)}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "is_active", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "password1", "password2", "is_staff", "is_superuser", "is_active"),
        }),
    )
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(CustomUser, CustomUserAdmin)

# Register your models here.
