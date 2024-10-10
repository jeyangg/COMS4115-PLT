FROM python:3.5

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y build-essential

# Step 6: Set the default command to run your language compiler
CMD ["python", "lexer.py"]