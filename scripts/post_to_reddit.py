import os
from pathlib import Path

import praw

# Reddit flair ids, keyed by the KIND of release rather than by any tag string.
# The announce workflow filters out prereleases and patch releases before this
# runs, so only these two kinds ever reach here.
FLAIR_ID_MAP = {
    "major": "e3d63234-5dc6-11f0-b36f-0a5798591b21",
    "minor": "0bc44ae2-5dc7-11f0-8a26-9685ac3bddf0",
}

SUBREDDIT = "LenoreApps"
DEFAULT_USER_AGENT = "LenoreAppsBot/1.0 by u/LenoreReleaseBot"


def release_kind(version):
    """
    Classifies a release from its version number.

    This is the whole bug this script had: it used to look the tag itself up in
    FLAIR_ID_MAP, but COMMIT_TAG holds a version tag ("v1.9.0") while the map is
    keyed "major"/"minor". The lookup never matched, so every release since the
    script was written took the "unknown tag, skipping" branch and returned
    successfully without posting anything.

    Args:
        version (str): A version such as "1.9.0" or "v1.9.0".

    Returns:
        (str): "major" for an x.0.0 release, "minor" for an x.y.0 release.

    Raises:
        ValueError: If the version cannot be parsed, or is a patch release —
            which the workflow should have filtered out before calling this.
    """
    parts = version.removeprefix("v").split(".")
    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        raise ValueError(f"cannot classify a release from version {version!r}")

    _, minor, patch = parts
    if patch != "0":
        raise ValueError(
            f"{version} is a patch release and is not announced on Reddit; "
            "the workflow gate should have skipped this"
        )
    return "major" if minor == "0" else "minor"


def main():
    # COMMIT_TAG is the release being announced, and the workflow checks that
    # exact tag out before running this. Taking the version from it rather than
    # from scripts/version.txt means there is one source of truth instead of two
    # that can disagree.
    tag = os.environ["COMMIT_TAG"]
    version = tag.removeprefix("v")
    changelog = os.environ["RELEASE_NOTES"]

    # Deliberately not a .get() with a skip: an unexpected version here means
    # the workflow gate let something through, and that should fail loudly.
    # Returning quietly is what hid this for a year.
    flair_id = FLAIR_ID_MAP[release_kind(version)]

    reddit = praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"],
        # The workflow passes REDDIT_USER_AGENT; the old hardcoded string stays
        # as the fallback so a missing secret cannot break the post.
        user_agent=os.environ.get("REDDIT_USER_AGENT") or DEFAULT_USER_AGENT,
    )

    title = f"LenoreShop v{version} Released!"
    body_template = Path("scripts/reddit_post_template.md").read_text()
    body = body_template.format(version=version, changelog=changelog)

    submission = reddit.subreddit(SUBREDDIT).submit(
        title=title, selftext=body, flair_id=flair_id
    )

    print(f"✅ Posted to Reddit: {submission.shortlink}")


if __name__ == "__main__":
    main()
