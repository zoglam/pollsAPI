FROM python:3.7.9-stretch

LABEL maintainer="pollsAPI: @kekmarakek"

ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_EMAIL=test@test.test
ENV DJANGO_SUPERUSER_PASSWORD=1234
ENV PORT=8080

WORKDIR /app

COPY . .

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r Requirements.txt

EXPOSE $PORT
CMD ["/app/runserver.sh"]