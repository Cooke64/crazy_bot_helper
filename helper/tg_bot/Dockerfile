FROM python:3.10-slim

LABEL owner="cooke09"

WORKDIR /app

COPY . .

RUN python -m pip install --upgrade pip

RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["python", "main_bot.py"]

# docker build -t main_bot .