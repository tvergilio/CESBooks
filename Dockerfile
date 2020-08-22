FROM python:3.7.8-slim-buster

# Create python virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install Docker (used by Jenkins)
RUN curl -fsSLO https://get.docker.com/builds/Linux/x86_64/docker-17.04.0-ce.tgz \
  && tar xzvf docker-17.04.0-ce.tgz \
  && mv docker/docker /usr/local/bin \
  && rm -r docker docker-17.04.0-ce.tgz

# Install apt dependencies
RUN apt-get update -y
RUN apt-get install python3-dev default-libmysqlclient-dev gcc  -y

# Copy files into flask directory
WORKDIR /usr/src/flask_uuid
COPY . .

# Install pip dependencies
RUN pip install -r requirements.txt

# Run
CMD ["python","waitress-server.py"]

EXPOSE 80

