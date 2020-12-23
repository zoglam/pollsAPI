#from django.urls import path
from django.conf.urls import url
from . import views


app_name = 'polls_app'

urlpatterns = [
    url(r'^auth/', views.auth),
    url(r'^pass_poll/(?P<id_poll>\d+)', views.pass_poll),
    url(r'^history/(?P<id_user>\d+)', views.get_history_by_id)
]

polls = [
    url(r'^polls/', views.get_polls),
    url(r'^create_poll/', views.create_poll),
    url(r'^alter_poll/(?P<id_poll>\d+)', views.alter_poll),
    url(r'^delete_poll/(?P<id_poll>\d+)', views.delete_poll),
]

questions = [
    url(r'^create_question/', views.create_question),
    url(r'^alter_question/(?P<id_question>\d+)', views.alter_question),
    url(r'^delete_question/(?P<id_question>\d+)', views.delete_question),
]

urlpatterns += polls
urlpatterns += questions
