FROM python:3.12.3-alpine

WORKDIR /app

COPY . ./

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "app.py"]
