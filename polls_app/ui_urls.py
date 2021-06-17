from django.conf.urls import url
from . import ui_views


app_name = 'polls_app'

urlpatterns = [
    url(r'^$', ui_views.menu),
    url(r'^polls/', ui_views.polls),
    url(r'^questions/', ui_views.questions),
    url(r'^history/', ui_views.history)
]

report = [
    url(r'^report/', ui_views.report),
    url(r'^excel_report/', ui_views.excel_report),
]

urlpatterns += report
