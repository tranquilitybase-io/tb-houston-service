# Useful commnds
## Build a mock container image using the Dockerfile for CICD workflow
docker build -t gcr.io/eagle-console-resources/tb-houston-mysql57:mock .
docker push gcr.io/eagle-console-resources/tb-houston-mysql57:mock

## Dump the database schema only
mysqldump eagle_db --column-statistics=false --no-data -u eagle-user -p > eagle_db_schema.tmp

## Dump the database data only
mysqldump eagle_db --column-statistics=false --no-create-info -u eagle-user -p > eagle_db_data.tmp

## Full DB dump
mysqldump eagle_db --column-statistics=false -u eagle-user -p > eagle_db_dump.tmp
