FROM python:alpine3.19

WORKDIR /app
COPY . ./
RUN apk add g++
RUN pip install -r requirements.txt

CMD ["python", "greeter_server.py" ]