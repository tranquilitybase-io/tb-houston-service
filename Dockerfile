FROM python:3.6
RUN apt-get update && apt-get install -y --no-install-recommends default-mysql-client=1.0.5 dos2unix=7.4.0-1 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /srv
COPY requirements.txt .
RUN pip install -r ./requirements.txt
COPY . .
RUN dos2unix app_docker.sh
RUN ["chmod", "+x", "./app_docker.sh"]
EXPOSE 3000
CMD ["/bin/bash", "./app_docker.sh"]
