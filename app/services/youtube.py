from datetime import datetime

import requests

from app.extensions import db
from app.models.video import Video

API_BASE = "https://www.googleapis.com/youtube/v3"
REQUEST_TIMEOUT = 15


class YouTubeSyncError(Exception):
    pass


def _get_uploads_playlist_id(api_key, channel_id):
    resp = requests.get(
        f"{API_BASE}/channels",
        params={"part": "contentDetails", "id": channel_id, "key": api_key},
        timeout=REQUEST_TIMEOUT,
    )
    resp.raise_for_status()
    items = resp.json().get("items", [])
    if not items:
        raise YouTubeSyncError(f"No channel found for id {channel_id!r}")
    return items[0]["contentDetails"]["relatedPlaylists"]["uploads"]


def _iter_playlist_items(api_key, playlist_id):
    page_token = None
    while True:
        params = {
            "part": "snippet",
            "playlistId": playlist_id,
            "maxResults": 50,
            "key": api_key,
        }
        if page_token:
            params["pageToken"] = page_token

        resp = requests.get(f"{API_BASE}/playlistItems", params=params, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()

        for item in data.get("items", []):
            yield item["snippet"]

        page_token = data.get("nextPageToken")
        if not page_token:
            return


def _best_thumbnail(thumbnails):
    for size in ("high", "medium", "default"):
        if size in thumbnails:
            return thumbnails[size]["url"]
    return None


def sync_videos(api_key, channel_id):
    """Upsert videos from a YouTube channel's uploads playlist into the Video table.

    Title/description/thumbnail/publish date are always refreshed from
    YouTube on every sync (YouTube is the source of truth for those).
    Category is only set on first insert so staff can recategorize a video
    without a later sync clobbering it.
    """
    if not api_key or not channel_id:
        raise YouTubeSyncError("YOUTUBE_API_KEY and YOUTUBE_CHANNEL_ID must both be set")

    uploads_playlist_id = _get_uploads_playlist_id(api_key, channel_id)

    created = 0
    updated = 0

    for snippet in _iter_playlist_items(api_key, uploads_playlist_id):
        video_id = snippet.get("resourceId", {}).get("videoId")
        if not video_id:
            continue

        published_at = snippet.get("publishedAt")
        published_date = (
            datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ").date()
            if published_at else datetime.utcnow().date()
        )

        video = Video.query.filter_by(youtube_video_id=video_id).first()
        if video is None:
            video = Video(
                youtube_video_id=video_id,
                category="Uncategorized",
                is_placeholder=False,
            )
            db.session.add(video)
            created += 1
        else:
            updated += 1

        video.title = snippet.get("title", video_id)
        video.description = snippet.get("description", "") or ""
        video.published_date = published_date
        video.external_url = f"https://www.youtube.com/watch?v={video_id}"
        video.thumbnail_url = _best_thumbnail(snippet.get("thumbnails", {}))
        video.is_placeholder = False

    db.session.commit()
    return created, updated
