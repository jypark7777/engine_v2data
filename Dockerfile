FROM python:3.8.9

#basic setting
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get -y install tzdata g++ git curl
RUN apt-get -y install default-jdk default-jre

RUN pip install --upgrade pip

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

#UWSGI
RUN pip install uwsgi
#RUN python3 manage.py collectstatic --noinput
ENV DJANGO_SETTINGS_MODULE=featuringeg_data.settings.release

RUN apt-get install -y nginx

# 기존에 존재하던 Nginx설정 파일들 삭제
RUN rm -rf /etc/nginx/sites-available/*
RUN rm -rf /etc/nginx/sites-enabled/*

COPY nginx.conf /etc/nginx/nginx.conf
COPY poza_score.conf /etc/nginx/sites-available/

RUN ln -s /etc/nginx/sites-available/poza_score.conf /etc/nginx/sites-enabled/

#supervisor 추가
RUN apt-get -y install supervisor
COPY supervisor-app.conf /etc/supervisor/conf.d/

WORKDIR /app

EXPOSE 80
#supervisor 사용
CMD ["bash", "-c", "/usr/bin/supervisord -c /etc/supervisor/conf.d/supervisor-app.conf"]

#EXPOSE 8000
#CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
#CMD ["uwsgi", "--ini", "/app/uwsgi.ini", "--http", ":8000"]

#로컬 이미지 실행 시 필요
#EXPOSE 8000
#CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000", "--settings=poza_score.settings.poza"]

#CMD ["uwsgi", "--ini", "/app/uwsgi.ini"]

#EXPOSE 80
#CMD ["service", "nginx", "start"]
#CMD ["nginx", "-g", "daemon off;"]

