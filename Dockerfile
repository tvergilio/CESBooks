FROM python:3.7.8-slim-buster

# Create python virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install apt dependencies
RUN apt-get update -y
RUN apt-get install python3-dev python3-psycopg2 gcc  -y

# Copy files into flask directory
WORKDIR /usr/src/flask_uuid
COPY . .

# Install pip dependencies
RUN pip install -r requirements.txt

# Run (Heroku runs as an unprivileged user - uncomment lines below to test locally)
# RUN useradd -m myuser
# USER myuser
CMD ["python","waitress-server.py"]

