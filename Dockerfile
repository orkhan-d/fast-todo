FROM python:latest

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

USER root
RUN chmod +x /app/runme.sh

ENTRYPOINT [ "bash", "/app/runme.sh" ]