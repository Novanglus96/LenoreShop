#!/bin/bash

VERSION_FILE="scripts/version.txt"

# Ensure the version file exists
if [ ! -f "$VERSION_FILE" ]; then
  echo "0.0.0" > $VERSION_FILE
fi

# Read current version
CURRENT_VERSION=$(cat "$VERSION_FILE")
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT_VERSION"

# Determine version type from commit messages
VERSION_TYPE="patch" # Default to patch

# Fetch commit messages
COMMIT_MSGS=$(git log --pretty=format:%s -n 1)
if echo "$COMMIT_MSGS" | grep -iq "\[major\]"; then
  VERSION_TYPE="major"
elif echo "$COMMIT_MSGS" | grep -iq "\[minor\]"; then
  VERSION_TYPE="minor"
fi

# Increment version based on type
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

echo "Version bumped to $NEW_VERSION ($VERSION_TYPE update)"

# Commit and push the updated version
git config user.name "GitHub Actions Bot"
git config user.email "<>"
git add "$VERSION_FILE"
git commit -m "Bump version to $NEW_VERSION"
git push
