#!/bin/bash
docker build -t micro/transferservice \
        --build-arg APP_NAME=FlaskApp \
        --build-arg FLASK_APP=main.py \
        .