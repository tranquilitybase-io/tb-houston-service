# Useful commands

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/3def1d65ed474beda546f2455f127e92)](https://app.codacy.com/gh/tranquilitybase-io/tb-houston-service?utm_source=github.com&utm_medium=referral&utm_content=tranquilitybase-io/tb-houston-service&utm_campaign=Badge_Grade_Settings)

## Build a container image using the Dockerfile
docker build -t gcr.io/tranquility-base-images/tb-houston-service:alpha .
docker push gcr.io/tranquility-base-images/tb-houston-service:alpha

## Experiment build
docker build -t gcr.io/tranquility-base-images/tb-houston-service:experimental .
docker push gcr.io/tranquility-base-images/tb-houston-service:experimental

## list existing containers and remove them
docker container list -a 
docker container rm xxxxxxx

## list existing images and remove them 
docker image list 
docker image rm xxxxxx

## Run Docker Image
## Authorize Docker command line interface
gcloud auth configure-docker

## Run the stack (houston-service + mysql57)
docker-compose -f stack.yml up

## Run the experimental stack (houston-service + mysql57)
docker-compose -f experimental_houston_service.yml up

## run the docker image
docker run -p 3000:3000 gcr.io/tranquility-base-images/tb-houston-service:alpha

## References
<https://cloud.google.com/sql/docs/mysql/connect-kubernetes-engine>
<https://cloud.google.com/sql/docs/mysql/configure-private-ip>

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/32de36097c284849b9b95ba94f6f982f)](https://www.codacy.com/gh/tranquilitybase-io/tb-houston-service?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tranquilitybase-io/tb-houston-service&amp;utm_campaign=Badge_Grade)
