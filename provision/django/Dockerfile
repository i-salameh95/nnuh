FROM python:3
ENV PYTHONUNBUFFERED 1

# install Dependencies
RUN apt-get update && apt-get install -y \
        gcc \
        gettext \
        curl \
        --no-install-recommends && rm -rf /var/lib/apt/lists/* \ && mkdir /code

 # install python modules
ADD requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

WORKDIR /code
EXPOSE 8000/tcp
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
