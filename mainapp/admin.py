from django.contrib import admin

from django.contrib import admin
from mainapp.models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text', 'selection_type']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'selection_type')
    list_filter = ['pub_date', 'selection_type']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
