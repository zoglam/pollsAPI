from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login
from .models import Poll, Question, AnonymousUser, History, QuestionType
# Create your views here.


@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((AllowAny,))
def auth(request):
    query = request.data
    requirements_fieds = ['username', 'password']

    if all((x in query for x in requirements_fieds)):
        user = authenticate(
            request, **{k: query[k] for k in requirements_fieds}
        )
        if user is not None:
            login(request, user)
            return Response({'status': 'True'}, status.HTTP_200_OK)
    return Response({'status': 'False'}, status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((AllowAny,))
def pass_poll(request, id_poll=None):
    query = request.data
    if 'user_id' not in request.session:
        request.session['user_id'] = AnonymousUser.objects.create().pk
    id_user = AnonymousUser.objects.get(pk=request.session['user_id'])
    try:
        for k in query:
            if Question.objects.get(pk=k).id_poll.pk == int(id_poll):
                History.objects.create(
                    user=id_user,
                    poll=Poll.objects.get(pk=id_poll),
                    question=Question.objects.get(pk=k),
                    text_question=query[k]
                )
        return Response({'status': 'True'}, status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'False',
            'details': f'{e}'
        }, status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((AllowAny,))
def get_history_by_id(request, id_question=None):
    query = request.data
    return Response({'status': 'False'}, status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((AllowAny,))
def get_polls(request):
    try:
        return Response({
            'polls': Poll.get_all(request)}, status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'False',
            'details': f'{e}'
        }, status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((IsAuthenticated,))
def create_poll(request):
    query = request.data
    try:
        if 'title' not in query:
            raise Exception('Not enough values')

        Poll.custom_create(query)
        return Response({'status': 'True'}, status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'False',
            'details': f'{e}'
        }, status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((IsAuthenticated,))
def alter_poll(request, id_poll=None):
    query = request.data
    try:
        Poll.custom_update(id_poll, query)
        return Response({'status': 'True'}, status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'False',
            'details': f'{e}'
        }, status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((IsAuthenticated,))
def delete_poll(request, id_poll=None):
    try:
        Poll.objects.get(pk=id_poll).delete()
        return Response({'status': 'True'}, status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'False',
            'details': f'{e}'
        }, status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((IsAuthenticated,))
def create_question(request):
    query = request.data
    requirement_fiels = ('id_poll', 'title', 'question_type')
    try:
        if not all((x in query for x in requirement_fiels)):
            raise Exception('Not enough values')

        Question.objects.create(
            id_poll=Poll.objects.get(pk=query['id_poll']),
            title=query['title'],
            question_type=QuestionType.objects.get(pk=query['question_type'])
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
def alter_question(request, id_question=None):
    query = request.data
    requirement_fiels = ('title', 'question_type')
    try:
        question = Question.objects.get(pk=id_question)
        if 'title' in query:
            question.title = query['title']
        if 'question_type' in query:
            question.question_type = QuestionType.objects.get(
                pk=query['question_type'])
        question.save()
        return Response({'status': 'True'}, status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'False',
            'details': f'{e}'
        }, status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((IsAuthenticated,))
def delete_question(request, id_question=None):
    try:
        Question.objects.get(pk=id_question).delete()
        return Response({'status': 'True'}, status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'False',
            'details': f'{e}'
        }, status.HTTP_400_BAD_REQUEST)
