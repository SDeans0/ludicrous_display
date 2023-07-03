FROM python:3.10

COPY src/requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY src/ /

CMD gunicorn --config app/gunicorn.conf.py  --worker-tmp-dir /dev/shm app.app:app
# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]
