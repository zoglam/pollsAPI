from datetime import datetime
from django.db import models
from django.db.models.deletion import CASCADE
import rest_framework.request
import rest_framework
from django.utils import timezone
# Create your models here.


class Poll(models.Model):
    title = models.CharField(max_length=200, verbose_name='title')
    description = models.CharField(max_length=500, default=None, null=True)
    date_published = models.DateTimeField(default=timezone.now, null=True)
    date_end = models.DateTimeField(
        default=None, verbose_name='date_end', null=True)

    @staticmethod
    def custom_create(query):
        query_dict = {
            k: query[k] for k in query
            if k in (f.name for f in Poll._meta.fields[1:])
        }
        for key in ['date_published', 'date_end']:
            if key in query_dict:
                query_dict[key] = datetime.strptime(
                    query_dict[key], '%Y-%m-%d')

        Poll.objects.create(**query_dict)

    @staticmethod
    def custom_update(id_poll, query):
        query_dict = {
            k: query[k] for k in query
            if k in (f.name for f in Poll._meta.fields[1:])
        }
        for key in ['date_published', 'date_end']:
            if key in query_dict:
                query_dict[key] = datetime.strptime(
                    query_dict[key], '%Y-%m-%d')

        poll = Poll.objects.get(pk=id_poll)
        if 'title' in query_dict:
            poll.title = query_dict['title']
        if 'description' in query_dict:
            poll.description = query_dict['description']
        if 'date_published' in query_dict:
            poll.date_published = query_dict['date_published']
        if 'date_end' in query_dict:
            poll.date_end = query_dict['date_end']
        poll.save()

    @staticmethod
    def get_all(request: rest_framework.request.Request) -> list:
        response_list = []
        polls = (
            Poll.objects.all().values()
            if request.user.is_authenticated
            else Poll.objects.filter(date_end__gte=datetime.now()).values()
        )
        for x in polls:
            x['questions'] = Question.objects.filter(id_poll=x['id']).values()
            response_list.append(x)
        return response_list

    def __str__(self):
        return f'id: {self.pk} title: {self.title}'


class QuestionType(models.Model):
    type = models.CharField(default='text', max_length=20)

    def __str__(self):
        return f'{self.type}'


class Question(models.Model):
    id_poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)

    def __str__(self):
        return f'id: {self.pk} title: {self.title}'


class AnonymousUser(models.Model):
    pass


class History(models.Model):
    user = models.ForeignKey(AnonymousUser, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text_question = models.CharField(max_length=200)
