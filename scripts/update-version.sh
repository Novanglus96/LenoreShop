#!/bin/bash
# Usage: ./scripts/update-version.sh <version>
# Updates version references across the project for a semantic-release prepare step.

VERSION=$1
if [ -z "$VERSION" ]; then
  echo "Usage: $0 <version>"
  exit 1
fi

VERSION_FILE="scripts/version.txt"
BACKEND_DOCKER_FILE="backend/Dockerfile"
FRONTEND_DOCKER_FILE="frontend/Dockerfile"
MODEL_VERSION_FILE="backend/api/fixtures/version.json"
API_PY_FILE="backend/backend/api.py"
PACKAGE_JSON_FILE="frontend/package.json"
APP_VUE_FILE="frontend/src/App.vue"

echo "$VERSION" > "$VERSION_FILE"
sed -i -r "s/^LABEL version=\"[^\"]*\"/LABEL version=\"$VERSION\"/" "$BACKEND_DOCKER_FILE"
sed -i -r "s/^LABEL version=\"[^\"]*\"/LABEL version=\"$VERSION\"/" "$FRONTEND_DOCKER_FILE"
sed -i -r "s/\"version_number\": \"[^\"]*\"/\"version_number\": \"$VERSION\"/" "$MODEL_VERSION_FILE"
sed -i -r "s/^api.version = \"[^\"]*\"/api.version = \"$VERSION\"/" "$API_PY_FILE"
sed -i -r "s/\"version\": \"[^\"]*\"/\"version\": \"$VERSION\"/" "$PACKAGE_JSON_FILE"
sed -i -r "s/\"[0-9]+\.[0-9]+\.[0-9]{1,3}\"/\"$VERSION\"/" "$APP_VUE_FILE"

echo "Updated version to $VERSION"
