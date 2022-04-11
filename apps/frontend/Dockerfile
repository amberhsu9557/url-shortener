FROM python:3.7-slim

ARG APP_NAME
ENV APP_NAME=$APP_NAME
ARG FLASK_APP
ENV FLASK_APP=$FLASK_APP

EXPOSE 5000

# Install the dependencies
ADD requirements.txt /tmp/requirements.txt
RUN mkdir -p /tmp/logs \
    && apt update && apt install -y gcc libpq-dev python3-dev \
    && pip install --upgrade pip setuptools \
    && pip install -r /tmp/requirements.txt \
    && rm -f /tmp/requirements.txt

# Set the working directory to /app
WORKDIR /app
# Copy the current directory contents into the container at /app 
ADD . /app

# run the command to start uvicorn
CMD ["uwsgi", "app.ini"]