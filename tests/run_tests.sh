#!/bin/bash 

# activate debugging
set -x
# exit when a command fails

# Activators
# POST TEST
echo "Activator POST TEST"
response=`curl -f -X POST http://0.0.0.0:5000/api/activator \
-H "Content-Type: application/json; charset=utf-8" \
--data-binary @- << EOF
{ \
   "activator": "activator1", \
   "apiManagement": [ "string" ], \
   "available": true, \
   "billing": "string", \
   "businessUnit": "string", \
   "category": "string", \
   "cd": [ "string" ], \
   "ci": [ "string" ], \
   "envs": [ "string" ], \
   "hosting": [ "string" ], \
   "lastUpdated": "2020-03-15 12:12:12", \
   "name": "TEST1", \
   "platforms": [ "platform1", "platform2" ], \
   "regions": [ "UK", "US", "FG", "DF" ], \
   "resources": [ \
     { "ipAddress": "xxx.xxx.xxx.xxx", "name": "AAA Cluster" }, \
     { "ipAddress": "xxx.xxx.xxx.xxx", "name": "BBB Cluster" }, \
     { "ipAddress": "xxx.xxx.xxx.xxx", "name": "GGG Cluster" }, \
     { "ipAddress": "xxx.xxx.xxx.xxx", "name": "GGG Cluster" } \
   ], \
   "sensitivity": "string", \
   "serverCapacity": 0, \
   "sourceControl": [ "sourceControl1" ], \
   "technologyOwner": "technologyOwner", \
   "technologyOwnerEmail": "technologyOwnerEmail", \
   "type": "microservices", \
   "lastUpdated": "2020-03-20 11:12:13", \
   "userCapacity": 1000, \
   "status": "Active"
 }
EOF`
ID=`echo $response | python get_id.py`
echo "ID: ${ID}"

if [ -z "${ID}" ]; then
    echo "Unable to obtain the id of the Activator just created."
    exit 1
fi

echo "Activator PUT TEST"
curl -v -f -X PUT http://0.0.0.0:5000/api/activator/${ID} \
-H "Content-Type: application/json; charset=utf-8" \
--data-binary @- << EOF
{ \
   "id": ${ID}, \
   "activator": "activator1", \
   "apiManagement": [ "string" ], \
   "available": true, \
   "billing": "string", \
   "businessUnit": "string", \
   "category": "string", \
   "cd": [ "string" ], \
   "ci": [ "string" ], \
   "envs": [ "string" ], \
   "hosting": [ "string" ], \
   "lastUpdated": "2020-03-15 12:12:12", \
   "name": "TEST1", \
   "platforms": [ "platform1", "platform2" ], \
   "regions": [ "UK", "US", "FG", "DF" ], \
   "resources": [ \
     { "ipAddress": "xxx.xxx.xxx.xxx", "name": "AAA Cluster" }, \
     { "ipAddress": "xxx.xxx.xxx.xxx", "name": "BBB Cluster" }, \
     { "ipAddress": "xxx.xxx.xxx.xxx", "name": "GGG Cluster" }, \
     { "ipAddress": "xxx.xxx.xxx.xxx", "name": "GGG Cluster" } \
   ], \
   "sensitivity": "string", \
   "serverCapacity": 0, \
   "sourceControl": [ "sourceControl1" ], \
   "technologyOwner": "technologyOwner", \
   "technologyOwnerEmail": "technologyOwnerEmail", \
   "type": "microservices", \
   "lastUpdated": "2020-03-20 11:12:13", \
   "userCapacity": 1000, \
   "status": "Active"
 }
EOF

echo "Activator GET TEST"
curl -v -f -X GET http://0.0.0.0:5000/api/activator/${ID} -H "Content-Type: application/json; charset=utf-8" 
echo 

echo "Activator DELETE TEST"
curl -v -f -X DELETE http://0.0.0.0:5000/api/activator/${ID} -H "Content-Type: application/json; charset=utf-8" 
echo


# application
echo "Application POST TEST"
response=`curl -f -X POST http://0.0.0.0:5000/api/application \
-H "Content-Type: application/json; charset=utf-8" \
--data-binary @- << EOF
{ \
  "activatorId": 0, \
  "description": "test application", \
  "env": "dev", \
  "name": "test", \
  "solutionId": 0, \
  "status": "status" 
} 
EOF`
echo

ID=`echo ${response} | python get_id.py`
echo "ID: ${ID}"

if [ -z "${ID}" ]; then
    echo "Unable to obtain the id of the Application just created."
    exit 1

echo "Application PUT TEST"
curl -v -f -X PUT http://0.0.0.0:5000/api/application/${ID} \
-H "Content-Type: application/json; charset=utf-8" \
--data-binary @- << EOF
{ \
  "id": ${ID}, \
  "activatorId": 0, \
  "description": "test activator", \
  "env": "dev", \
  "name": "test", \
  "solutionId": 0, \
  "status": "status" 
} 
EOF
echo 

# GET TEST
echo "Application GET TEST"
curl -v -f -X GET http://0.0.0.0:5000/api/application/${ID} -H "Content-Type: application/json; charset=utf-8" 
echo

echo "Application DELETE TEST"
curl -v -f -X DELETE http://0.0.0.0:5000/api/application/${ID} -H "Content-Type: application/json; charset=utf-8" 
echo

# BusinessUnit
# POST BusinessUnit
echo "businessUnit POST TEST"
response=`curl -X POST --header "Accept: application/json" "http://0.0.0.0:5000/api/businessUnit" \
-H "Content-Type: application/json; charset=utf-8" \
--data-binary @- << EOF
{ \
  "key": "TEST", \
  "value": "TEST"
} 
EOF`
echo

# PUT 
KEY=`echo ${response} | python get_key.py`
echo "KEY: "${KEY}""

if [ -z "${KEY}" ]; then
    echo "Unable to obtain the key of the businessUnit just created."
    exit 1

echo "businessUnit PUT TEST"
curl -X PUT --header "Accept: application/json" "http://0.0.0.0:5000/api/businessUnit/${KEY}" \
-H "Content-Type: application/json; charset=utf-8" \
--data-binary @- << EOF
{ \
  "key": "${KEY}",  \
  "value": "TESTTEST" 
} 
EOF
echo

# GET BusinessUnit
echo "businessUnit GET ALL TEST"
curl -X GET --header "Accept: application/json" "http://0.0.0.0:5000/api/businessUnit"
echo

# GET BusinessUnit
echo "businessUnit GET TEST"
curl -X GET --header "Accept: application/json" "http://0.0.0.0:5000/api/businessUnit/${KEY}"
echo

# DELETE BusinessUnit
echo "businessUnit DELETE TEST"
curl -X DELETE --header "Accept: application/json" "http://0.0.0.0:5000/api/businessUnit/${KEY}"
echo


# CI
# POST CI
echo "CI POST TEST"
response=`curl -X POST --header "Accept: application/json" "http://0.0.0.0:5000/api/ci" \
-H "Content-Type: application/json; charset=utf-8" \
--data-binary @- << EOF
{ \
  "key": "TEST", \
  "value": "TEST"
} 
EOF`
echo

# PUT 
KEY=`echo ${response} | python get_key.py`
echo "KEY: "${KEY}""

if [ -z "${KEY}" ]; then
    echo "Unable to obtain the key of the ci just created."
    exit 1

echo "CI PUT TEST"
curl -X PUT --header "Accept: application/json" "http://0.0.0.0:5000/api/ci/${KEY}" \
-H "Content-Type: application/json; charset=utf-8" \
--data-binary @- << EOF
{ \
  "key": "${KEY}",  \
  "value": "TESTTEST"  
} 
EOF
echo

# GET CI
echo "CI GET ALL TEST"
curl -X GET --header "Accept: application/json" "http://0.0.0.0:5000/api/ci"
echo

# GET CI
echo "CI GET ONE TEST"
curl -X GET --header "Accept: application/json" "http://0.0.0.0:5000/api/ci/${KEY}"
echo

# DELETE CI
echo "CI DELETE TEST"
curl -X DELETE --header "Accept: application/json" "http://0.0.0.0:5000/api/ci/${KEY}"
echo


# CD
# POST CD
echo "CD POST TEST"
response=`curl -X POST --header "Accept: application/json" "http://0.0.0.0:5000/api/cd" \
-H "Content-Type: application/json; charset=utf-8" \
--data-binary @- << EOF
{ \
  "key": "TEST", \
  "value": "TEST"
} 
EOF`
echo

# PUT 
KEY=`echo ${response} | python get_key.py`
echo "KEY: "${KEY}""

if [ -z "${KEY}" ]; then
    echo "Unable to obtain the key of the ci just created."
    exit 1

echo "CD PUT TEST"
curl -X PUT --header "Accept: application/json" "http://0.0.0.0:5000/api/cd/${KEY}" \
-H "Content-Type: application/json; charset=utf-8" \
--data-binary @- << EOF
{ \
  "key": "${KEY}",  \
  "value": "TESTTEST" 
} 
EOF
echo

# GET CD
echo "CD GET ALL TEST"
curl -X GET --header "Accept: application/json" "http://0.0.0.0:5000/api/cd"
echo

# GET CD
echo "CD GET TEST"
curl -X GET --header "Accept: application/json" "http://0.0.0.0:5000/api/cd/${KEY}"
echo

# DELETE CD
echo "CD DELETE TEST"
curl -X DELETE --header "Accept: application/json" "http://0.0.0.0:5000/api/cd/${KEY}"
echo


#curl -f -X GET http://0.0.0.0:5000/api/solutions
#curl -f -X GET http://0.0.0.0:5000/api/solution

# Disable debugging
set +x
