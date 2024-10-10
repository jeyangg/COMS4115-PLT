FROM python:3.5

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y python3 python3-pip

CMD ["python", "lexer.py"]