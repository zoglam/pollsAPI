from django.test import TestCase, Client
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from datetime import datetime
from .models import Question, Answer, AnswerType
import json
# Create your tests here.


class RequestForQuestion(TestCase):
    def setUp(self) -> None:
        self.url_create = '/api/create_question/'

        self.c = Client()
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()

        self.c.login(username='testuser', password='12345')
        AnswerType.objects.create(type='text')

    def _response(self, data):
        request = self.c.post(self.url_create, data)
        return json.loads(request.getvalue().decode("utf-8"))

    def test_valid_data(self):
        """Post request with valid data"""
        resp = self._response({
            'title': 'Test question',
            'description': 'made by admin',
            'date_published': '2020-06-01',
            'date_end': '2020-06-02'
        })
        print(f'{resp}')
        self.assertEqual(resp['status'], 'True')

    def test_invalid_data(self):
        """Post request with invalid data"""
        resp = self._response({
            'title': 'Test question',
            'description': 'made by admin',
            'date_published': 'BROKEN_FIELD',
            'date_end': '2020-06-02'
        })
        print(f'{resp}')
        self.assertEqual(resp['status'], 'False')

        resp = self._response({
            'title': 'Test question',
            'description': 'made by admin',
            'date_published': '2020-06-01',
            'date_end': 'BROKEN_FIELD'
        })
        print(f'{resp}')
        self.assertEqual(resp['status'], 'False')

        resp = self._response({
            'title': 'Test question',
            'description': 'made by admin',
            'date_published': '2020-06-01'
        })
        print(f'{resp}')
        self.assertEqual(resp['status'], 'False')


class DBCase(TestCase):
    def setUp(self) -> None:
        Question.objects.create(
            title="Test question",
            description="made by admin",
            date_published=datetime(2020, 6, 1),
            date_end=datetime(2020, 6, 2)
        )

    def test_question_create(self):
        obj = Question.objects.get(title="Test question")
        self.assertEqual(obj.get_json(), {
            'id': 1,
            'title': 'Test question',
            'description': 'made by admin',
            'date_published': '2020-06-01',
            'date_end': '2020-06-02'
        })
