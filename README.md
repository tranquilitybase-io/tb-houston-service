# Build a container image using the Dockerfile
gcloud builds submit --tag gcr.io/eagle-console-resources/tb-houston-service-image .

# list existing containers and remove them
docker container list -a 
docker container rm xxxxxxx

# list existing images and remove them 
docker image list 
docker image rm xxxxxx

# Run Docker Image
# Authorize Docker command line interface
gcloud auth configure-docker


# run the docker image
docker run -p 3000:3000 gcr.io/eagle-console-resources/tb-houston-service-image


# References
https://cloud.google.com/sql/docs/mysql/connect-kubernetes-engine
https://cloud.google.com/sql/docs/mysql/configure-private-ip
