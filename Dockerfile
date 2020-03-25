FROM python:3.6
RUN apt-get update && apt-get install -y vim default-mysql-client
COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY config/local_development.py /config/
COPY config/gcp_development.py /config/
COPY *.py /
COPY swagger.yml /
COPY app.sh /
RUN ["chmod", "+x", "/app.sh"]
EXPOSE 3000
CMD ["/bin/bash", "/app.sh"]
