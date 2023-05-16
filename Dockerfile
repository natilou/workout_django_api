FROM python:3.10.11-slim

WORKDIR /src

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --dev

COPY . .

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
