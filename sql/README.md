# Build a container image using the Dockerfile
docker build -t gcr.io/tranquility-base-images/tb-houston-service:mysql57 .
docker push gcr.io/tranquility-base-images/tb-houston-service:mysql57

# run the docker image
docker run --name mysql57 \
    -p 3306:3306 \
    -e MYSQL_ROOT_PASSWORD=my-secret-pw \
    -e MYSQL_USER=eagle-user \
    -e MYSQL_PASSWORD=eagle-user-secret-pw \
    -e MYSQL_DATABASE=eagle_db \
    -d gcr.io/tranquility-base-images/tb-houston-service:mysql57

# Dump the database
mysqldump eagle_db --column-statistics=false -u eagle-user -p > eagle_db_dump.tmp
