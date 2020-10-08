FROM python:3-alpine
MAINTAINER Osama Sarwar

ADD . /app
WORKDIR /app

RUN pip install flask

COPY app.py /app/app.py

#ENTRYPOINT [ "./app/app.py" ]

CMD python app.py
