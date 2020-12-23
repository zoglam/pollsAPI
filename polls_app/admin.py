from django.contrib import admin
from .models import QuestionType, Poll, Question
# Register your models here.

admin.site.register(QuestionType)
admin.site.register(Poll)
admin.site.register(Question)
