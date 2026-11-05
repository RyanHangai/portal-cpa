FROM python:3.14
WORKDIR /app

CMD ["bash", "/app/.docker/app.init.dev.sh"]
