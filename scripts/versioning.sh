#!/bin/bash

VERSION_FILE="scripts/version.txt"

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

# Commit and push the updated version file
git config user.name "GitHub Actions Bot"
git config user.email "actions@github.com"
git add "$VERSION_FILE"
git commit -m "Bump version to $NEW_VERSION"
git push

# Create a Git tag
git tag -a "v$NEW_VERSION" -m "Release version $NEW_VERSION"
git push origin "v$NEW_VERSION"

# Create a GitHub release
gh release create "v$NEW_VERSION" --title "Release $NEW_VERSION" --generate-notes