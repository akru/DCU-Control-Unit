#!/bin/sh
# Args: 
#       server - server:port string
#       uid    - uid for testing


echo "{\"uid\": \"$2\"}"
curl -H 'Content-type: application/json' -X POST -d "{\"uid\": \"$2\"}" "http://$1/dcu"
