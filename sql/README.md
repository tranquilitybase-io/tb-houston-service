# Useful commnds
## Build a container image using the Dockerfile
docker build -t gcr.io/tranquility-base-images/tb-houston-service:mysql57 .
docker push gcr.io/tranquility-base-images/tb-houston-service:mysql57

## Build a container image for experimental using the Dockerfile
docker build -t gcr.io/tranquility-base-images/tb-houston-mysql57:experimental .
docker push gcr.io/tranquility-base-images/tb-houston-mysql57:experimental

## Build a container image for landingzone using the Dockerfile
docker build -t gcr.io/tranquility-base-images/tb-houston-mysql57:landingzone .
docker push gcr.io/tranquility-base-images/tb-houston-mysql57:landingzone

## run the docker image
docker run --name mysql57 \
    -p 3306:3306 \
    -e MYSQL_ROOT_PASSWORD=my-secret-pw \
    -e MYSQL_USER=eagle-user \
    -e MYSQL_PASSWORD=eagle-user-secret-pw \
    -e MYSQL_DATABASE=eagle_db \
    -d gcr.io/tranquility-base-images/tb-houston-service:mysql57

## Dump the database schema only
mysqldump eagle_db --column-statistics=false --no-data -u eagle-user -p > eagle_db_schema.tmp

## Dump the database data only
mysqldump eagle_db --column-statistics=false --no-create-info -u eagle-user -p > eagle_db_data.tmp

## Full DB dump
mysqldump eagle_db --column-statistics=false -u eagle-user -p > eagle_db_dump.tmp
or
mysqldump eagle_db -h 0.0.0.0 --column-statistics=false -u eagle-user -p > eagle_db_dump.tmp
