#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 version"
    exit 1
fi

# Assign command-line arguments to variables
version_num="$1"
app_name_prefix="lenoreshop"
backend_suffix="_backend"
frontend_suffix="_frontend"
backend_name="$app_name_prefix$backend_suffix"
frontend_name="$app_name_prefix$frontend_suffix"

# Remove latest tag from frontend/backend
docker rmi registry.danielleandjohn.love/$backend_name:latest
docker rmi registry.danielleandjohn.love/$frontend_name:latest
docker rmi novanglus96/$backend_name:latest
docker rmi novanglus96/$frontend_name:latest

# Tag the new production version as version
docker tag $backend_name:production registry.danielleandjohn.love/$backend_name:$version_num
docker tag $frontend_name:production registry.danielleandjohn.love/$frontend_name:$version_num
docker tag $backend_name:production novanglus96/$backend_name:$version_num
docker tag $frontend_name:production novanglus96/$frontend_name:$version_num

# Tag the new production version as latest
docker tag $backend_name:production registry.danielleandjohn.love/$backend_name:latest
docker tag $frontend_name:production registry.danielleandjohn.love/$frontend_name:latest
docker tag $backend_name:production novanglus96/$backend_name:latest
docker tag $frontend_name:production novanglus96/$frontend_name:latest

# Remove the local tag of new image
docker rmi $backend_name:production
docker rmi $frontend_name:production

# Push the version tag of new image
docker push registry.danielleandjohn.love/$frontend_name:$version_num
docker push registry.danielleandjohn.love/$backend_name:$version_num
docker push novanglus96/$frontend_name:$version_num
docker push novanglus96/$backend_name:$version_num

# Push the latest tag of new image
docker push registry.danielleandjohn.love/$frontend_name:latest
docker push registry.danielleandjohn.love/$backend_name:latest
docker push novanglus96/$frontend_name:latest
docker push novanglus96/$backend_name:latest

# Print the version number
echo "Published $app_name_prefix $version_num"
