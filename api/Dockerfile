FROM python:3.13-alpine
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "flask_api:flask_api" ]