from django.contrib import admin

from .models import Question, Choice


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
        return f"{obj.votes}(Voted by:{', '.join([user.username for user in obj.voter.all()])})"
    
    voters.short_description ="Votes & Voters"
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Question, QuestionAdmin)

# Register your models here.
