FROM python:3.13-alpine
RUN apk update && \
    apk add --no-cache wget && \
    apk add --no-cache build-base libffi-dev openssl-dev && \
    apk add python3 py3-pip gcc musl-dev
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "flask_api:flask_api" ]