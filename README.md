# Build using a Dockerfile
gcloud builds submit --tag gcr.io/eagle-console-resources/tb-houston-service-image .

# Build using a build config file
gcloud builds submit --config cloudbuild.yml .

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
docker run -p 5000:5000 gcr.io/eagle-console-resources/tb-houston-service-image


# References
https://cloud.google.com/sql/docs/mysql/connect-kubernetes-engine
https://cloud.google.com/sql/docs/mysql/configure-private-ip
