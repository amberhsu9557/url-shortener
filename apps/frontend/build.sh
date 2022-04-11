#!/bin/bash
docker build -t micro/frontend \
        --build-arg APP_NAME=FlaskApp \
        --build-arg FLASK_APP=main.py \
        .