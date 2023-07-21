FROM python:alpine AS builder

RUN apk update
RUN apk add su-exec
RUN rm -rf /var/cache/apk/*s


WORKDIR /django
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
# ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
ENTRYPOINT ["./entry_point.sh"]
