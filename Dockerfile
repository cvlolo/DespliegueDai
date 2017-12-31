FROM ubuntu:16.04
MAINTAINER Manuel Casado 


RUN apt-get update
RUN apt-get install -y python python-pip nginx gunicorn supervisor
RUN apt-get install -y python-setuptools
RUN apt-get install -y python-dev
RUN apt-get install -y build-essential
RUN apt-get install -y libpq-dev
RUN pip install --upgrade
RUN apt-get install net-tools


RUN apt-get install -y git
RUN git clone https://github.com/cvlolo/DespliegueDai.git


RUN mkdir -p /deploy/practica3
COPY practica3 /deploy/practica3
RUN pip install -r /deploy/practica3/requirements.txt

RUN mkdir -p /var/www/flask/static
COPY /practica3/static /var/www/flask/static

RUN rm /etc/nginx/sites-enabled/default
COPY flask.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled/flask.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf



COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 80
CMD sudo supervisorctl reread
CMD sudo supervisorctl update
CMD sudo supervisorctl start flaskdeploy
