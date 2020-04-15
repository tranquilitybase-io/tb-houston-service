# Useful commands
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
