FROM python:3.14
WORKDIR /app

RUN curl -fsSL https://raw.githubusercontent.com/pressly/goose/master/install.sh | sh

CMD ["/app/.docker/app.init.dev.sh"]
