"""Helpers for working with YouTube URLs."""

from urllib.parse import parse_qs, urlparse


def extract_video_id(url: str) -> str | None:
    """Extracts a YouTube video ID from a URL string."""
    parsed = urlparse(url)
    if parsed.netloc in {"youtu.be", "www.youtu.be"}:
        return parsed.path.lstrip("/").split("/")[0] or None

    if parsed.netloc in {"www.youtube.com", "youtube.com", "m.youtube.com"}:
        if parsed.path == "/watch":
            return parse_qs(parsed.query).get("v", [None])[0]
        if parsed.path.startswith("/shorts/"):
            return parsed.path.split("/")[-1]

    return None
