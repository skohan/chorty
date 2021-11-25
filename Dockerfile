# Dockerfile for chorty

FROM python:3.9
ENV PYTHONUNBUFFERED=1

WORKDIR /code

ENV PORT 8080

COPY requirements.txt /code/requirements.txt

RUN pip install -r requirements.txt

COPY . /code/

RUN python manage.py makemigrations
RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
