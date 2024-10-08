FROM python:3-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./api/generated/requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./api/generated /usr/src/app
COPY ./core /usr/src/app/core
COPY ./service /usr/src/app/service

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["-m", "server"]