FROM ubuntu:12.04
MAINTAINER Manuel Casado

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y python python-pip python-virtualenv nginx gunicorn supervisor libpq-dev


RUN mkdir -p /deploy/practica3
COPY practica3 /deploy/practica3
RUN pip install -r /deploy/app/requirements.txt


RUN rm /etc/nginx/sites-enabled/default
COPY flask.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled/flask.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

RUN mkdir -p /var/www/flask/static
COPY /practica3/static /var/www/flask/static



RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf


CMD ["/usr/bin/supervisord"]



