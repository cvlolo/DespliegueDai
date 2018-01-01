
############################################################
# Dockerfile to build flask image
# Based on Ubuntu 16.04
############################################################

# Set the base image to Ubuntu

FROM laztoum/base

MAINTAINER Manuel Casado

RUN mkdir /flaskApp \
	&& cd flaskApp

RUN apt-get update \
	&& apt-get install -y python-pip \
	gcc \
	nginx \
	supervisor \
	&& rm -rf /var/lib/apt/lists/*

COPY practica3/requirements.txt /flaskApp/
RUN pip install -r /flaskApp/requirements.txt

COPY flask.conf /etc/nginx/sites-available/default

RUN mkdir -p /var/www/flask/static
COPY /practica3/static /var/www/flask/static

# Custom Supervisord config
COPY supervisord.conf /etc/supervisor/conf.d/

# Make NGINX run on the foreground
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

COPY practica3/* /flaskApp/

WORKDIR /flaskApp
VOLUME /flaskApp

# Expose ports
EXPOSE 80  
#EXPOSE 443

# Set the default command to execute when creating a new container
CMD ["supervisord", "-n"]






