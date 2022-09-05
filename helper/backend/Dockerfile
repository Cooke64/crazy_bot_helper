FROM python:3.10-slim

LABEL owner="cooke09"

WORKDIR /app

COPY . .

RUN python -m pip install --upgrade pip

RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["python", "manage.py", "runserver", "0:8000"]

#docker build -t backend .
# docker run --name backend -it -p 8000:8000 backend