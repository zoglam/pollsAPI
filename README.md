# Contents pollsAPI
- [Cmd](#Native)
- [Docker](#Docker)
- [API Documentation](#API-Documentation)
    - [`POST` api/auth/](#POST-apiauth)
    - [`POST` api/pass_poll/<id_poll>](#POST-apipass_pollid_poll)
    - [`GET` api/history/<id_user>](#GET-apihistoryid_user)
    -
    - [`GET` api/polls/](#GET-apipolls)
    - [`POST` api/create_poll/](#POST-apicreate_poll)
    - [`POST` api/alter_poll/<id_poll>](#POST-apialter_pollid_poll)
    - [`DELETE` api/delete_poll/<id_poll>](#DELETE-apidelete_pollid_poll)
    -
    - [`POST` api/create_question/](#POST-apicreate_question)
    - [`POST` api/alter_question/<id_question>](#POST-apialter_questionid_question)
    - [`DELETE` api/delete_question/<id_question>](#DELETE-apidelete_questionid_question)
- [Database scheme](#Database-scheme)
# Cmd
Prepare
```
python -m pip install -r Requirements.txt
```
```
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata initial_data.json
python manage.py createsuperuser --username admin --email test@test.test
```
Test
```
python manage.py test
python manage.py test polls_app.tests.CreateTable -v 1
python manage.py test polls_app.tests.AlterTable -v 1
python manage.py test polls_app.tests.DeleteTable -v 1
python manage.py test polls_app.tests.PassPoll -v 1
python manage.py test polls_app.tests.GetHistory -v 1
```
Run
```
python manage.py runserver 0.0.0.0:8080
```
**[⬆ Back to Top](#Contents-pollsAPI)**
# Docker
Build
```
docker build -t pollsapi:1.0 .
```
Run
```
docker run  -it -p 8080:8080 \
    --env DJANGO_SUPERUSER_USERNAME=admin \
    --env DJANGO_SUPERUSER_EMAIL=test@test.test \
    --env DJANGO_SUPERUSER_PASSWORD=1234 \
    --env PORT=8080 pollsapi:1.0
```
**[⬆ Back to Top](#Contents-pollsAPI)**
# API Documentation
## `POST` api/auth/
**Метод для авторизации администратора**
```
Parameters
```
|Name|Description|
|----|-----------|
|username `*required`|Имя пользователя|
|password `*required`|Пароль|
```
Response
```
<table>
<tr><td> Status </td> <td> Response </td></tr>
<tr>
<td style="text-align:center"> 200 </td>
<td>
Запрос успешно обработан<br/>
<b>Example Value:</b>

```json
{
    "status": "True"
}
```
</td>
</tr>
<tr>
<td style="text-align:center"> 400 </td>
<td>
Ошибка запроса<br/>
<b>Example Value:</b>

```json
{
    "status": "False"
}
```
</td>
</tr>
</table>

**[⬆ Back to Top](#Contents-pollsAPI)**
<hr>

## `POST` api/pass_poll/<id_poll>
**Метод для прохождения опроса пользователем**
```
Parameters
```
<table>
<tr><td> <b>Name</b> </td> <td> <b>Description</b> </td></tr>
<tr><td>id_poll <font color="red">*required</f></td><td>ID опроса, который был пройден. Передается в адресной строке</td><tr>
<tr>
<td> </td>
<td>
json по пройденному опросу<br/>
<b>Example Value:</b>

```json
{
    "<id_question>": "<value>",
    "<id_question>": "<value>",
    "<id_question>": "<value>"
}
```
</td>
</tr>
</table>

```
Response
```
<table>
<tr><td> Status </td> <td> Response </td></tr>
<tr>    
<td style="text-align:center"> 200 </td>
<td>
Запрос успешно обработан<br/>
<b>Example Value:</b>

```json
{
    "status": "True"
}
```
</td>
</tr>
<tr>
<td style="text-align:center"> 400 </td>
<td>
Ошибка запроса<br/>
<b>Example Value:</b>

```json
{
    "status": "False",
    "details": "Error discription"
}
```
</td>
</tr>
</table>

**[⬆ Back to Top](#Contents-pollsAPI)**
<hr>

## `GET` api/history/<id_user>
**Метод для получения всех опросов, которые прошел пользователь, с подробным описанием выбранных ответов**
```
Parameters
```
|Name|Description|
|-|-|
|id_user ```*required```|ID пользователя|
```
Response
```
<table>
<tr><td> Status </td> <td> Response </td></tr>
<tr>
<td style="text-align:center"> 200 </td>
<td>
Запрос успешно обработан<br/>
<b>Example Value:</b>

```json
{
    "status": "True",
    "details": [
        {
            "id": 1, 
            "user_id": 1, 
            "poll_id": 1, 
            "question_id": 1, 
            "text_question": "test_text1"
        },
        {
            "id": 2, 
            "user_id": 1, 
            "poll_id": 1, 
            "question_id": 2, 
            "text_question": "test_text2"
        }
    ]
}
```
</td>
</tr>
<tr>
<td style="text-align:center"> 400 </td>
<td>
Ошибка запроса<br/>
<b>Example Value:</b>

```json
{
    "status": "False",
    "details": "Error discription"
}
```
</td>
</tr>
</table>

**[⬆ Back to Top](#Contents-pollsAPI)**
<hr>


## `GET` api/polls/
**Метод для получения всех опросов в системе**
```
Response
```
<table>
<tr><td> Status </td> <td> Response </td></tr>
<tr>
<td style="text-align:center"> 200 </td>
<td>
Запрос успешно обработан<br/>
<b>Example Value:</b>

```json
{
    "status": "True",
    "details": [
        {
            "id": 1,
            "title": "poll1",
            "description": null,
            "date_published": "2020-12-23T21:15:49.321611",
            "date_end": null,
            "questions": [
                {
                    "id": 1,
                    "id_poll_id": 1,
                    "title": "question1",
                    "question_type_id": 1
                },
                {
                    "id": 2,
                    "id_poll_id": 1,
                    "title": "question2",
                    "question_type_id": 1
                },
                {
                    "id": 3,
                    "id_poll_id": 1,
                    "title": "question3",
                    "question_type_id": 1
                }
            ]
        },
        {
            "id": 2,
            "title": "poll2",
            "description": null,
            "date_published": "2020-12-23T21:15:49.321611",
            "date_end": null,
            "questions": [
                {
                    "id": 4,
                    "id_poll_id": 2,
                    "title": "question1",
                    "question_type_id": 1
                },
                {
                    "id": 5,
                    "id_poll_id": 2,
                    "title": "question2",
                    "question_type_id": 1
                }
            ]
        }
    ]
}
```
</td>
</tr>
<tr>
<td style="text-align:center"> 400 </td>
<td>
Ошибка запроса<br/>
<b>Example Value:</b>

```json
{
    "status": "False",
    "details": "Error discription"
}
```
</td>
</tr>
</table>

**[⬆ Back to Top](#Contents-pollsAPI)**
<hr>

## `POST` api/create_poll/
**Метод для создания опроса**
```
Parameters
```
|Name|Description|
|-|-|
|title `*required`|Название опроса|
|description |Описание опроса|
|date_published |Дата публикации|
|date_end |Дата окончания|
```
Response
```
<table>
<tr><td> Status </td> <td> Response </td></tr>
<tr>
<td style="text-align:center"> 200 </td>
<td>
Запрос успешно обработан<br/>
<b>Example Value:</b>

```json
{
    "status": "True"
}
```
</td>
</tr>
<tr>
<td style="text-align:center"> 400 </td>
<td>
Ошибка запроса<br/>
<b>Example Value:</b>

```json
{
    "status": "False",
    "details": "time data 'BROKEN_FIELD' does not match format '%Y-%m-%d'"
}
```

```json
{
    "status": "False",
    "details": "Not enough values"
}
```
</td>
</tr>
</table>

**[⬆ Back to Top](#Contents-pollsAPI)**
<hr>

## `POST` api/alter_poll/<id_poll>
**Метод для изменения полей опроса**
```
Parameters
```
|Name|Description|
|-|-|
|id_poll `*required`|ID опроса|
|title |Название опроса|
|description |Описание опроса|
|date_published |Дата публикации|
|date_end |Дата окончания|
```
Response
```
<table>
<tr><td> Status </td> <td> Response </td></tr>
<tr>
<td style="text-align:center"> 200 </td>
<td>
Запрос успешно обработан<br/>
<b>Example Value:</b>

```json
{
    "status": "True"
}
```
</td>
</tr>
<tr>
<td style="text-align:center"> 400 </td>
<td>
Ошибка запроса<br/>
<b>Example Value:</b>

```json
{
    "status": "False",
    "details": "Error discription"
}
```
</td>
</tr>
</table>

**[⬆ Back to Top](#Contents-pollsAPI)**
<hr>

## `DELETE` api/delete_poll/<id_poll>
**Метод для удаления опроса**
```
Parameters
```
|Name|Description|
|-|-|
|id_poll ```*required```|ID опроса|
```
Response
```
<table>
<tr><td> Status </td> <td> Response </td></tr>
<tr>
<td style="text-align:center"> 200 </td>
<td>
Запрос успешно обработан<br/>
<b>Example Value:</b>

```json
{
    "status": "True"
}
```
</td>
</tr>
<tr>
<td style="text-align:center"> 400 </td>
<td>
Ошибка запроса<br/>
<b>Example Value:</b>

```json
{
    "status": "False",
    "details": "Poll matching query does not exist."
}
```
</td>
</tr>
</table>

**[⬆ Back to Top](#Contents-pollsAPI)**
<hr>


## `POST` api/create_question/
**Метод для создания вопроса**
```
Parameters
```
|Name|Description|
|-|-|
|id_poll `*required`|ID опроса|
|title `*required`|Описание вопроса|
|question_type `*required`|id типа вопроса(1-text,2-radio,3-checkbox)|
```
Response
```
<table>
<tr><td> Status </td> <td> Response </td></tr>
<tr>
<td style="text-align:center"> 200 </td>
<td>
Запрос успешно обработан<br/>
<b>Example Value:</b>

```json
{
    "status": "True"
}
```
</td>
</tr>
<tr>
<td style="text-align:center"> 400 </td>
<td>
Ошибка запроса<br/>
<b>Example Value:</b>

```json
{
    "status": "False",
    "details": "Not enough values"
}
```
</td>
</tr>
</table>

**[⬆ Back to Top](#Contents-pollsAPI)**
<hr>

## `POST` api/alter_question/<id_question>
**Метод для изменения полей вопроса**
```
Parameters
```
|Name|Description|
|-|-|
|id_question ```*required```|ID вопроса|
```
Response
```
<table>
<tr><td> Status </td> <td> Response </td></tr>
<tr>
<td style="text-align:center"> 200 </td>
<td>
Запрос успешно обработан<br/>
<b>Example Value:</b>

```json
{
    "status": "True"
}
```
</td>
</tr>
<tr>
<td style="text-align:center"> 400 </td>
<td>
Ошибка запроса<br/>
<b>Example Value:</b>

```json
{
    "status": "False",
    "details": "Error discription"
}
```
</td>
</tr>
</table>

**[⬆ Back to Top](#Contents-pollsAPI)**
<hr>

## `DELETE` api/delete_question/<id_question>
**Метод для удаления вопроса**
```
Parameters
```
|Name|Description|
|-|-|
|id_question ```*required```|ID вопроса|
```
Response
```
<table>
<tr><td> Status </td> <td> Response </td></tr>
<tr>
<td style="text-align:center"> 200 </td>
<td>
Запрос успешно обработан<br/>
<b>Example Value:</b>

```json
{
    "status": "True"
}
```
</td>
</tr>
<tr>
<td style="text-align:center"> 400 </td>
<td>
Ошибка запроса<br/>
<b>Example Value:</b>

```json
{
    "status": "False",
    "details": "Question matching query does not exist."
}
```
</td>
</tr>
</table>

**[⬆ Back to Top](#Contents-pollsAPI)**

# Database scheme
[<img src="https://live.staticflickr.com/65535/50752040621_6032d1612a_h.jpg" width=900>](https://live.staticflickr.com/65535/50752040621_6032d1612a_h.jpg)