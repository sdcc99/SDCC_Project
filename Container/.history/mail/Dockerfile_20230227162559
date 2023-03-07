FROM python:3.9-slim-buster

WORKDIR /mail

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "sendemail.py" ]