from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login

from .models import Question, Answer
# Create your views here.


@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((AllowAny,))
def auth(request):
    query = request.data
    if all((x in query for x in ['username', 'password'])):
        user = authenticate(
            request, username=query['username'],
            password=query['password']
        )
        if user is not None:
            login(request, user)
            return Response({'status': 'True'}, status.HTTP_200_OK)
    return Response({'status': 'False'}, status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((AllowAny,))
def getQuestions(request):
    try:
        return Response({
            'polls': Question.get_all(request)}, status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'False',
            'details': f'{e}'
        }, status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((IsAuthenticated,))
def createQuestion(request):
    query = request.data
    try:
        if 'title' not in query:
            raise Exception('Not enough values')

        Question.custom_create(query)
        return Response({'status': 'True'}, status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'False',
            'details': f'{e}'
        }, status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((IsAuthenticated,))
def alterQuestion(request, id_question=None):
    query = request.data
    try:
        Question.custom_update(id_question, query)
        return Response({'status': 'True'}, status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'False',
            'details': f'{e}'
        }, status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((IsAuthenticated,))
def deleteQuestion(request, id_question=None):
    try:
        Question.objects.delete(pk=id_question)
        return Response({'status': 'True'}, status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'False',
            'details': f'{e}'
        }, status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((IsAuthenticated,))
def createAnswer(request):
    query = request.data
    try:
        if not all((x in query for x in
                    ('id_question', 'title', 'answer_type'))):
            raise Exception('Not enough values')

        Answer.objects.create(
            id_question=query['id_question'],
            title=query['title'],
            answer_type=query['answer_type'],
        )
        return Response({'status': 'True'}, status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'False',
            'details': f'{e}'
        }, status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((IsAuthenticated,))
def alterAnswer(request, id_answer=None):
    query = request.data
    try:
        Answer.objects.update(pk=id_answer, **{
            k: query[k] for k in query
            if k in ['title', 'votes', 'answer_type']
        })
        return Response({'status': 'True'}, status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'False',
            'details': f'{e}'
        }, status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((IsAuthenticated,))
def deleteAnswer(request, id_answer=None):
    try:
        Answer.objects.delete(pk=id_answer)
        return Response({'status': 'True'}, status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'False',
            'details': f'{e}'
        }, status.HTTP_400_BAD_REQUEST)
