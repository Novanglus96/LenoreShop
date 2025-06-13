#!/bin/bash

VERSION_FILE="scripts/version.txt"
BACKEND_DOCKER_FILE="backend/Dockerfile"
FRONTEND_DOCKER_FILE="frontend/Dockerfile"
MODEL_VERSION_FILE="backend/api/fixtures/version.json"
API_PY_FILE="backend/backend/api.py"
PACKAGE_JSON_FILE="frontend/package.json"
APPNAVIGATION_VUE_FILE="frontend/src/components/AppNavigation.vue"
APP_VUE_FILE="frontend/src/App.vue"

# Ensure the version file exists
if [ ! -f "$VERSION_FILE" ]; then
  echo "0.0.0" > "$VERSION_FILE"
fi

# Read the current version
CURRENT_VERSION=$(cat "$VERSION_FILE")
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT_VERSION"

# Default version type to "patch"
VERSION_TYPE="patch"

# Fetch the latest commit message
COMMIT_MSG=$(git log -1 --pretty=%s)
echo "Commit Message: $COMMIT_MSG"  # Debugging line

# Simplify pattern matching
if [[ "$COMMIT_MSG" == *"[major]"* || "$COMMIT_MSG" == "major:"* || "$COMMIT_MSG" == "major"* ]]; then
  VERSION_TYPE="major"
elif [[ "$COMMIT_MSG" == *"[minor]"* || "$COMMIT_MSG" == "minor:"* || "$COMMIT_MSG" == "minor"* ]]; then
  VERSION_TYPE="minor"
fi

echo "Detected Version Type: $VERSION_TYPE"  # Debugging line

# Increment the version based on the detected type
case $VERSION_TYPE in
  major)
    MAJOR=$((MAJOR + 1))
    MINOR=0
    PATCH=0
    ;;
  minor)
    MINOR=$((MINOR + 1))
    PATCH=0
    ;;
  patch)
    PATCH=$((PATCH + 1))
    ;;
esac

# Write the new version back to the file
NEW_VERSION="$MAJOR.$MINOR.$PATCH"
echo "$NEW_VERSION" > "$VERSION_FILE"

# Log the version update
echo "Version bumped to $NEW_VERSION ($VERSION_TYPE update)"

# Backend docker file
sed -i -r "s/^LABEL version=\"[^\"]*\"/LABEL version=\"$NEW_VERSION\"/" $BACKEND_DOCKER_FILE

# Backend docker file
sed -i -r "s/^LABEL version=\"[^\"]*\"/LABEL version=\"$NEW_VERSION\"/" $FRONTEND_DOCKER_FILE

# Model version
sed -i -r "s/\"version_number\": \"[0-9]+\.[0-9]+\.[0-9]{1,3}/\"version_number\": \"$NEW_VERSION/" $MODEL_VERSION_FILE

# api.py
sed -i -r "s/api.version = \"[0-9]+[.]?[0-9]?[.]?[0-9]?/api.version = \"$NEW_VERSION/" $API_PY_FILE

# package.json
sed -i -r "s/\"version\": \"[0-9]+[.]?[0-9]?[.]?[0-9]?/\"version\": \"$NEW_VERSION/" $PACKAGE_JSON_FILE

# AppNavigation
sed -i -r "s/>v[0-9]+[.]?[0-9]?[.]?[0-9]?</>v$NEW_VERSION</" $APPNAVIGATION_VUE_FILE

# App.vue
sed -i -r "s/\"[0-9]+\.[0-9]+\.[0-9]{1,3}\"/\"$NEW_VERSION\"/" $APP_VUE_FILE

# Commit and push the updated version file
git config user.name "GitHub Actions Bot"
git config user.email "actions@github.com"
git add "$VERSION_FILE"
git add "$BACKEND_DOCKER_FILE"
git add "$FRONTEND_DOCKER_FILE"
git add "$MODEL_VERSION_FILE"
git add "$API_PY_FILE"
git add "$PACKAGE_JSON_FILE"
git add "$APPNAVIGATION_VUE_FILE"
git add "$APP_VUE_FILE"
git commit -m "Bump version to $NEW_VERSION"
git push

# Create a Git tag
git tag -a "v$NEW_VERSION" -m "Release version $NEW_VERSION"
git push origin "v$NEW_VERSION"

# Create a GitHub release
gh release create "v$NEW_VERSION" --title "Release $NEW_VERSION" --generate-notes