FROM python:3.9-alpine

RUN mkdir /course
COPY . /course
RUN pip install -r /course/requirements.txt
RUN chmod +x /course/start.sh

WORKDIR /course
ENTRYPOINT ["./start.sh"]
