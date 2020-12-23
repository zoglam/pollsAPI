from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import QuestionType, History, Poll, Question
import json
# Create your tests here.


class CreateTable(TestCase):
    def setUp(self) -> None:
        self.url_create = '/api/create_poll/'

        self.c = Client()
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()

        self.c.login(username='testuser', password='12345')
        QuestionType.objects.create(type='text')

    def _response(self, data):
        print(f'\t{self.url_create}')
        request = self.c.post(self.url_create, data)
        return json.loads(request.getvalue().decode("utf-8"))

    def test_valid_data(self):
        """Post request with valid data"""
        print('\n\t-- RequestForPoll valid data test --')

        valid_data = [
            {
                'title': 'Test question',
                'description': 'made by admin',
                'date_published': '2020-06-01',
                'date_end': '2020-06-02'
            },
            {
                'title': 'Test question',
                'date_published': '2020-06-01',
                'date_end': '2020-06-02'
            },
            {
                'title': 'Test question',
                'date_end': '2020-06-02'
            },
            {
                'title': 'Test question'
            }
        ]
        for index, item in enumerate(valid_data):
            resp = self._response(item)
            print(f'\t>>> test {index+1}: {resp}')
            self.assertEqual(resp['status'], 'True')

    def test_invalid_data(self):
        """Post request with invalid data"""
        print('\n\t-- RequestForPoll invalid data test --')
        invalid_data = [
            {
                'title': 'Test question',
                'description': 'made by admin',
                'date_published': 'BROKEN_FIELD',
                'date_end': '2020-06-02'
            },
            {
                'title': 'Test question',
                'description': 'made by admin',
                'date_published': '2020-06-01',
                'date_end': 'BROKEN_FIELD'
            },
            {
                'description': 'made by admin',
                'date_published': '2020-06-01'
            }
        ]

        for index, item in enumerate(invalid_data):
            resp = self._response(item)
            print(f'\t>>> test {index+1}: {resp}')
            self.assertEqual(resp['status'], 'False')


class PassPoll(TestCase):

    fixtures = ['initial_test_data.json']

    def setUp(self) -> None:
        self.url = '/api/pass_poll/'
        self.c = Client()

    def _response(self, data, i):
        print(f'\t{self.url}{i}')
        request = self.c.post(f'{self.url}{i}', data)
        return json.loads(request.getvalue().decode("utf-8"))

    def test_passing(self):
        print('\n\t-- PassPoll test --')
        valid_data = [
            {
                '1': 'res1',
                '2': 'res2',
                '3': 'res3'
            },
            {
                '4': 'res4',
                '5': 'res5'
            }
        ]
        for i, d in enumerate(valid_data):
            resp = self._response(d, i+1)
            print(f'\t>>> test {i+1}: {resp}')
            self.assertEqual(resp['status'], 'True')

        print(f'\t\t>> History table:')
        for i in History.objects.all().values():
            print(f'\t\t>> {i}')
        self.assertEqual(len(History.objects.all()), 5)


class AlterTable(TestCase):

    fixtures = ['initial_test_data.json']

    def setUp(self) -> None:
        self.url_alter_poll = '/api/alter_poll'
        self.url_alter_question = '/api/alter_question'

        self.c = Client()
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()

        self.c.login(username='testuser', password='12345')

    def _response(self, data, url):
        print(f'\t{url}')
        request = self.c.post(url, data)
        return json.loads(request.getvalue().decode("utf-8"))

    def test_alter_poll(self):
        print('\n\t-- AlterTable alter_poll test --')
        data = {'title': 'new_title'}
        resp = self._response(data, f'{self.url_alter_poll}/1')
        print(f'\t>>> test 1: {resp}')
        poll = Poll.objects.get(pk=1)
        print(f'\t\t>>> {poll}')
        self.assertEqual(resp['status'], 'True')
        self.assertEqual(poll.title, 'new_title')

        data = {'title': 'new_title', 'description': 'new_desk'}
        resp = self._response(data, f'{self.url_alter_poll}/2')
        print(f'\t>>> test 2: {resp}')
        poll = Poll.objects.get(pk=2)
        print(f'\t\t>>> {poll}')
        self.assertEqual(resp['status'], 'True')
        self.assertEqual(poll.title, 'new_title')
        self.assertEqual(poll.description, 'new_desk')

    def test_alter_question(self):
        print('\n\t-- AlterTable alter_question test --')
        data = {'title': 'new_title'}
        resp = self._response(data, f'{self.url_alter_question}/1')
        print(f'\t>>> test 1: {resp}')
        question = Question.objects.get(pk=1)
        print(f'\t\t>>> {question}')
        self.assertEqual(resp['status'], 'True')
        self.assertEqual(question.title, 'new_title')

        data = {'title': 'new_title', 'question_type': '2'}
        resp = self._response(data, f'{self.url_alter_question}/2')
        print(f'\t>>> test 2: {resp}')
        question = Question.objects.get(pk=2)
        print(f'\t\t>>> {question}')
        self.assertEqual(resp['status'], 'True')
        self.assertEqual(question.title, 'new_title')
        self.assertEqual(question.question_type.pk, 2)


class DeleteTable(TestCase):

    fixtures = ['initial_test_data.json']

    def setUp(self) -> None:
        self.url_delete_poll = '/api/delete_poll'
        self.url_delete_question = '/api/delete_question'

        self.c = Client()
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()

        self.c.login(username='testuser', password='12345')

    def _response(self, url):
        print(f'\t{url}')
        request = self.c.delete(url)
        return json.loads(request.getvalue().decode("utf-8"))

    def test_delete_poll(self):
        print('\n\t-- DeleteTable delete_poll test --')
        resp = self._response(f'{self.url_delete_poll}/1')
        print(f'\t>>> test 1: {resp}')
        self.assertEqual(resp['status'], 'True')

        resp = self._response(f'{self.url_delete_poll}/99')
        print(f'\t>>> test 2: {resp}')
        self.assertEqual(resp['status'], 'False')

    def test_delete_question(self):
        print('\n\t-- DeleteTable delete_question test --')
        resp = self._response(f'{self.url_delete_question}/4')
        print(f'\t>>> test 1: {resp}')
        self.assertEqual(resp['status'], 'True')

        resp = self._response(f'{self.url_delete_question}/99')
        print(f'\t>>> test 2: {resp}')
        self.assertEqual(resp['status'], 'False')


class GetHistory(TestCase):

    fixtures = ['initial_test_data2.json']

    def setUp(self) -> None:
        self.url_history = '/api/history'
        self.c = Client()

    def _response(self, url):
        print(f'\t{url}')
        request = self.c.get(url)
        return json.loads(request.getvalue().decode("utf-8"))

    def test_get_request(self):
        print('\n\t-- GetHistory get_request test --')
        resp = self._response(f'{self.url_history}/1')
        print(f'\t>>> test 1: {resp["status"]}')
        for history in resp["details"]:
            print(f'\t\t>> {history}')
        self.assertEqual(resp['status'], 'True')
        self.assertEqual(len(resp["details"]), 2)
