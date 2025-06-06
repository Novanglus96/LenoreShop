#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 version"
    exit 1
fi

# Assign command-line arguments to variables
version_num="$1"

# Backend docker file
sed -i -r "s/version=\"[0-9]+[.]?[0-9]?[.]?[0-9]?\"/version=\"$version_num\"/" backend/Dockerfile

# Backend docker file
sed -i -r "s/version=\"[0-9]+[.]?[0-9]?[.]?[0-9]?\"/version=\"$version_num\"/" frontend/Dockerfile

# Model version
sed -i -r "s/\"version_number\": \"[0-9]+\.[0-9]+\.[0-9]{1,3}/\"version_number\": \"$version_num/" backend/api/fixtures/version.json

# api.py
sed -i -r "s/api.version = \"[0-9]+[.]?[0-9]?[.]?[0-9]?/api.version = \"$version_num/" backend/backend/api.py

# package.json
sed -i -r "s/\"version\": \"[0-9]+[.]?[0-9]?[.]?[0-9]?/\"version\": \"$version_num/" frontend/package.json

# AppNavigation
sed -i -r "s/>v[0-9]+[.]?[0-9]?[.]?[0-9]?</>v$version_num</" frontend/src/components/AppNavigation.vue

# App.vue
sed -i -r "s/\"[0-9]+\.[0-9]+\.[0-9]{1,3}\"/\"$version_num\"/" frontend/src/App.vue

# Print the version number
echo "Changed to $version_num"
