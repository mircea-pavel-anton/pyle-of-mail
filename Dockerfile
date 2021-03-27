FROM python:3.8-buster

RUN mkdir -p /home/pom

COPY src/* /home/pom/
COPY requirements.txt /tmp/requirements.txt

RUN pip3 install -r /tmp/requirements.txt

CMD ["python3", "/home/pom/main.py"]