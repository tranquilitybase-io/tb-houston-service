FROM python:3.6
RUN apt-get update && apt-get install -y default-mysql-client
WORKDIR /srv
COPY . .
RUN pip install -r ./requirements.txt
RUN ["chmod", "+x", "./app_docker.sh"]
EXPOSE 3000
CMD ["/bin/bash", "./app_docker.sh"]
