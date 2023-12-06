# FROM python:3.10.6-buster
# COPY taxifare /taxifare
# COPY requirements.txt /requirements.txt
# COPY setup.py /setup.py
# RUN pip install --upgrade pip
# RUN pip install .

FROM python:3.10.6-buster

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/AndyW1990/rl-control.git .

# RUN pip install -r requirements.txt

RUN pip install streamlit

HEALTHCHECK CMD curl --fail http://localhost:8000/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8000", "--server.address=0.0.0.0"]

EXPOSE 8000
