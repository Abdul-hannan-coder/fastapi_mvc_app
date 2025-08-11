#!/bin/bash
until nc -z mongodb 27017; do
    echo "Waiting for MongoDB to start..."
    sleep 1
done
echo "MongoDB is up! Starting the app..."
exec "$@"
