FROM python:3.10.6-buster

WORKDIR /rl_control

# Update OS with base packages
RUN apt-get update \
    && apt-get upgrade \
    && apt-get install -y \
    build-essential \
    software-properties-common

# Copy across the package
COPY . .












RUN rm -rf /var/lib/apt/lists/*

CMD uvicorn




COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt \
    && pip install bpy

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    blender \
    && rm -rf /var/lib/apt/lists/*
# RUN pip install --upgrade pip


CMD uvicorn RL-CONTROL.api.fast:app --host 0.0.0.0 --port $PORT
