FROM python:3.7
RUN apt-get update && apt-get install -y default-mysql-client
WORKDIR /srv
COPY . .
RUN pip install -r ./requirements.txt
RUN ["chmod", "+x", "./app.sh"]
EXPOSE 80
CMD ["/bin/bash", "./app.sh"]
