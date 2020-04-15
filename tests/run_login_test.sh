#!/bin/bash 

# activate debugging
set -x
# exit when a command fails

response=$(curl -f -X POST "http://0.0.0.0:3000/api/login" \
--header "Accept: text/plain" -H "Content-Type: application/json; charset=utf-8" \
--data-binary @- << EOF
{ \
   "username": "admin@your.company", \
   "password": "pass1"
 }
EOF)
echo "$response"



curl -I -X POST http://0.0.0.0:5000/api/login
curl -I -X POST http://0.0.0.0:3000/api/login
