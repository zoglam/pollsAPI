from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login
from .models import Poll, Question, AnonymousUser, History, QuestionType
# Create your views here.
from django.http import HttpResponse, FileResponse
from django.template import loader

from datetime import datetime
import xlsxwriter
import pdfkit
from xhtml2pdf import pisa
from io import StringIO, BytesIO
from django_pdfkit import PDFView


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((AllowAny,))
def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render())


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((AllowAny,))
def polls(request):
    template = loader.get_template("polls.html")
    return HttpResponse(template.render())


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((AllowAny,))
def questions(request):
    template = loader.get_template("questions.html")
    return HttpResponse(template.render())


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((AllowAny,))
def history(request):
    template = loader.get_template("history.html")
    return HttpResponse(template.render())


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((AllowAny,))
def report(request):
    couriers = Poll.objects.all().values()
    orders = Question.objects.all().values()

    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")

    template = loader.get_template("report_template.html")

    template_vars = {
        'couriers': couriers,
        'orders': orders,
        'datetime': dt_string
    }

    html = template.render(template_vars)

    pdf = pdfkit.from_string(html, False)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    return HttpResponse(pdf, content_type='application/pdf')


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((AllowAny,))
def excel_report(request):
    polls = Poll.objects.all().values()
    questions = Question.objects.all().values()

    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")

    data = []

    data.append(["Опросы"])
    data.append([
        'Идентификатор',
        'Название',
        'Описание',
        'Дата публикации',
        'Дата окончания'
    ])

    for poll in polls:
        data.append([
            poll['id'],
            poll['title'],
            poll['description'],
            poll['date_published'].strftime("%m/%d/%Y, %H:%M:%S"),
            poll['date_end']
        ])
    data.append([""])

    data.append(["Вопросы"])
    data.append([
        'Идентификатор',
        'Идентификатор Опроса',
        'Название',
        'Тип вопроса'
    ])

    for question in questions:
        data.append([
            question['id'],
            question['id_poll_id'],
            question['title'],
            question['question_type_id']
        ])
    data.append([""])

    max_len_array = max(map(len, data))
    data = list(map(lambda x: x+([""]*(max_len_array-len(x))), data))

    workbook = xlsxwriter.Workbook(f'{dt_string}.xlsx')
    worksheet = workbook.add_worksheet()

    col = 0
    row = 0

    # Iterate over the data and write it out row by row.
    for args in data:
        for column in range(len(args)):
            worksheet.write(row, column, args[column])
        row += 1

    new_data = [
        ["Опросы", len(polls)],
        ["Вопросы", len(questions)],
    ]

    chart = workbook.add_chart({'type': 'pie'})
    chart.add_series({
        'categories': f'=Sheet1!$A${row + 1}:$A${row + 2}',
        'values': f'=Sheet1!$B${row + 1}:$B${row + 2}',
        'points': [
            {'fill': {'color': 'green'}},
            {'fill': {'color': 'red'}},
        ],
    })
    worksheet.insert_chart('G1', chart)

    for item, val in new_data:
        worksheet.write(row, col, item)
        worksheet.write(row, col + 1, val)
        row += 1

    workbook.close()

    output = None
    with open(f'./{dt_string}.xlsx', "rb") as excel:
        output = excel.read()
    response = HttpResponse(output,
                            content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename={dt_string}.xlsx'
    return response
