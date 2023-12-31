from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from app import models as model
from django.contrib.admin.widgets import AutocompleteSelect
from django.db import models
# Register your models here.


@admin.register(model.SubAnswer)
class SubAnswerAdmin(admin.ModelAdmin):
    list_display = ("answer_title","answer")
    raw_id_fields = ("answer",)



class SubAnswerTabularInline(admin.TabularInline):
    model = model.SubAnswer
    fields = ("answer_title","sub_answer_weight", "answer_weight")

class AnswerTabularInline(admin.TabularInline):
    model = model.Answer
    fields = ('answer_title','answer_weight_for_hashing', 'answer_weight',  'answer_dependens_on', 'answer_weight_store')
    
    raw_id_fields = ('answer_dependens_on', 'stage_fit')
    fk_name = "questionIdd"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('questionIdd', 'answer_dependens_on', 'stage_fit')
        return queryset


@admin.register(model.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_title', 'stage', 'question_index',  'question_type') 
    inlines = [AnswerTabularInline]
    search_fields = ('question_title', 'question_dependens_on_question__question_title')
    raw_id_fields = ('question_dependens_on_answer', 'question_dependens_on_question')
    # def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
    #     return super().get_queryset(request).select_related('question_dependens_on_answer', "question_dependens_on_question")

@admin.register(model.Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('stage_name', 'parent', 'slug', 'stage_index')


@admin.register(model.Answer)
class AnswerAdmin(admin.ModelAdmin):
    search_fields= ('answer_title','questionIdd__question_title')
    autocomplete_fields = ['answer_dependens_on']
    list_display = ('answer_title', 'get_question_title', 'answer_weight', 'answer_weight_store')
    inlines = [SubAnswerTabularInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('questionIdd')
        return queryset
    
    def get_question_title(self, obj):
        return obj.questionIdd.question_title

    get_question_title.short_description = 'Question'

