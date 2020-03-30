# Build a container image using the Dockerfile
docker build -t gcr.io/tranquility-base-images/tb-houston-service:alpha .
docker push gcr.io/tranquility-base-images/tb-houston-service:alpha

# list existing containers and remove them
docker container list -a 
docker container rm xxxxxxx

# list existing images and remove them 
docker image list 
docker image rm xxxxxx

# Run Docker Image
# Authorize Docker command line interface
gcloud auth configure-docker

# Run the stack (houston-service + mysql57)
docker-compose -f stack.yml up

# run the docker image
docker run -p 3000:3000 gcr.io/tranquility-base-images/tb-houston-service:alpha


# References
https://cloud.google.com/sql/docs/mysql/connect-kubernetes-engine
https://cloud.google.com/sql/docs/mysql/configure-private-ip
