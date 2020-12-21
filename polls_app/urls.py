#from django.urls import path
from django.conf.urls import url
from . import views


app_name = 'polls_app'

urlpatterns = [
    url(r'^auth/', views.auth),
]

questions = [
    url(r'^questions/', views.getQuestions),
    url(r'^create_question/', views.createQuestion),
    url(r'^alter_question/', views.alterQuestion),
    url(r'^delete_question/(?P<id_question>\d+)', views.deleteQuestion),
]

answers = [
    url(r'^create_answer/', views.createAnswer),
    url(r'^alter_answer/', views.alterAnswer),
    url(r'^delete_answer/(?P<id_answer>\d+)', views.deleteAnswer),
]

urlpatterns += questions
urlpatterns += answers
