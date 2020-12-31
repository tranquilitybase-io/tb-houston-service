FROM python:3.6

WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r ./requirements.txt
COPY . .

ENV NUMBER_OF_WORKERS=${NUMBER_OF_WORKERS:-5} \
    PORT=${PORT:-3000}

RUN adduser --disabled-password houston
USER houston

EXPOSE ${PORT}
CMD gunicorn --workers="${NUMBER_OF_WORKERS}" --bind="0.0.0.0:${PORT}" app:connex_app
