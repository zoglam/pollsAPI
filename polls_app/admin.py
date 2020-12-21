from django.contrib import admin
from .models import AnswerType, Question, Answer
# Register your models here.

admin.site.register(AnswerType)
admin.site.register(Question)
admin.site.register(Answer)
