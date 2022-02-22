FROM ubuntu:18.04

WORKDIR /app

COPY . .
RUN apt-get update && \
    apt-get install lsof -y && \
    apt-get install -y python3.6 && \
    apt-get install -y python3-pip &&\
    pip3 install --upgrade cython &&\
    pip3 install --upgrade pip &&\
    pip3 install -r requirements.txt

EXPOSE 8080
ENTRYPOINT ['python worker.py']
#CMD ['create_features']
