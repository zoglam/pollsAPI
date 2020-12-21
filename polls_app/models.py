from datetime import datetime
from django.db import models
from django.db.models.deletion import CASCADE
import rest_framework.request
import rest_framework

# Create your models here.


class Question(models.Model):
    title = models.CharField(max_length=200, verbose_name='title')
    description = models.CharField(max_length=500, default=None)
    date_published = models.DateTimeField(default=datetime.now())
    date_end = models.DateTimeField(default=None, verbose_name='date_end')

    @staticmethod
    def get_all(request: rest_framework.request.Request) -> list:
        questions = (
            Question.objects.all().values()
            if request.user.is_authenticated
            else Question.objects.filter(date_end__gte=datetime.now()).values()
        )

        response_list = []
        for x in questions:
            x['answers'] = Answer.objects.filter(id_question=x['id']).values()
            response_list.append(x)
        return response_list

    def __str__(self):
        return f'id: {self.pk} title: {self.title}'


class AnswerType(models.Model):
    type = models.CharField(default='text', max_length=20)

    def __str__(self):
        return f'{self.type}'


class Answer(models.Model):
    id_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    answer_type = models.ForeignKey(AnswerType, on_delete=models.CASCADE)

    def __str__(self):
        return f'id: {self.pk} title: {self.title}'
