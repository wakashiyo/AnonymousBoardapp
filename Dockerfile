FROM python:3.10-alpine

WORKDIR /usr/src/app
ENV PYTHONDOONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 必要なビルドツールをインストール
RUN apk add --no-cache gcc musl-dev libffi-dev

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
RUN pip install django-allauth
RUN mkdir -p /var/run/gunicorn

CMD ["gunicorn", "boardapp.wsgi", "--bind=unix:/var/run/gunicorn/gunicorn.sock"]