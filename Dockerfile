# docker build -t anime_web:1.0.0 .
# docker save -o anime_web.tar anime_web
# docker load -i anime_web.tar
FROM python:3.13-alpine

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["gunicorn", "-c", "config.py", "app:app"]
