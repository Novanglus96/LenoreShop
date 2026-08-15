"""
Helpers for turning an uploaded photo into the two renditions the app stores.

Photos come off a phone camera, so they arrive rotated by EXIF only, in HEIC or
PNG as often as JPEG, and at 3-5MB. None of that is what we want to send back
down to a phone standing in a shop, so every upload is re-encoded here rather
than stored as-is:

    full   - what a tap-to-enlarge opens. Bounded by FULL_MAX_EDGE.
    thumb  - what a shopping list row shows. Bounded by THUMB_MAX_EDGE.

Both are baseline JPEG. The source format is deliberately not preserved: a
uniform output format means the frontend never has to care what the camera
produced, and dropping alpha is harmless for photographs.
"""

import io
import uuid

from PIL import Image, ImageOps, UnidentifiedImageError
from django.core.files.base import ContentFile

# A phone photo is a few MB; anything much past this is not a product snapshot.
MAX_UPLOAD_BYTES = 12 * 1024 * 1024

# Longest edge, in px. The full size is bounded by what a phone screen can
# actually show, not by what the camera captured.
FULL_MAX_EDGE = 1280
THUMB_MAX_EDGE = 256

FULL_QUALITY = 82
THUMB_QUALITY = 72


class ImageUploadError(ValueError):
    """Raised when an upload is not something we can store as a photo."""


def _encode(image, max_edge, quality):
    """
    Downscales a copy of `image` to fit `max_edge` and encodes it as JPEG.

    Args:
        image (Image): An already-normalised Pillow image.
        max_edge (int): Bound for the longest edge, in px.
        quality (int): JPEG quality.

    Returns:
        (ContentFile): The encoded JPEG, named with a fresh uuid.
    """
    copy = image.copy()
    # thumbnail() is in-place, keeps aspect ratio, and never upscales — a photo
    # already smaller than the bound is left alone rather than blown up.
    copy.thumbnail((max_edge, max_edge), Image.LANCZOS)

    buffer = io.BytesIO()
    copy.save(buffer, format="JPEG", quality=quality, optimize=True)
    return ContentFile(buffer.getvalue(), name=f"{uuid.uuid4().hex}.jpg")


def build_renditions(uploaded_file):
    """
    Validates an uploaded photo and builds its full and thumbnail renditions.

    Args:
        uploaded_file (UploadedFile): The file as it arrived on the request.

    Returns:
        (tuple): A `(full, thumb)` pair of ContentFiles ready to assign to an
            ImageField.

    Raises:
        ImageUploadError: If the upload is too large, or is not an image Pillow
            can decode.
    """
    if uploaded_file.size > MAX_UPLOAD_BYTES:
        limit_mb = MAX_UPLOAD_BYTES // (1024 * 1024)
        raise ImageUploadError(f"Image is larger than {limit_mb}MB.")

    try:
        image = Image.open(uploaded_file)
        # Forces a decode now, so a truncated or mislabelled file fails here
        # rather than halfway through encoding.
        image.load()
    except (UnidentifiedImageError, OSError) as error:
        raise ImageUploadError("That file is not an image we can read.") from error

    # Phone cameras record orientation in EXIF instead of rotating the pixels;
    # without this the photo is stored sideways.
    image = ImageOps.exif_transpose(image)

    if image.mode in ("RGBA", "LA", "P"):
        # JPEG has no alpha. Flatten onto white rather than letting Pillow
        # error out or turn transparency black.
        image = image.convert("RGBA")
        flattened = Image.new("RGB", image.size, (255, 255, 255))
        flattened.paste(image, mask=image.split()[-1])
        image = flattened
    elif image.mode != "RGB":
        image = image.convert("RGB")

    return (
        _encode(image, FULL_MAX_EDGE, FULL_QUALITY),
        _encode(image, THUMB_MAX_EDGE, THUMB_QUALITY),
    )


def delete_renditions(obj):
    """
    Deletes the stored image files for an object without touching the row.

    Used both when a photo is replaced and when its owner is deleted, so the
    media volume does not accumulate orphans.

    Args:
        obj (Model): An Item or FreezerItem.
    """
    for field in ("image", "thumbnail"):
        stored = getattr(obj, field, None)
        if stored:
            # save=False: the caller decides whether the row is worth writing.
            stored.delete(save=False)
