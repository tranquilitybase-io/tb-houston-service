FROM mysql:5.7
WORKDIR /docker-entrypoint-initdb.d
COPY eagle_db_dump.sql .
EXPOSE 3306
