FROM python:3.8-buster

ENV PIP_REQUIRE_VIRTUALENV false

RUN apt-get -y update && apt-get -y install libgl1-mesa-glx ffmpeg libsm6 libxext6
ADD requirements.txt /requirements.txt
ADD 6 /6
ADD recognise /recognise
ADD templates /templates
ADD tun /tun
ADD manage.py /manage.py
RUN pip install -r requirements.txt
RUN python manage.py migrate
EXPOSE 8000
RUN python manage.py runserver 0.0.0.0:8000
