# -*- coding: utf-8 -*-
"""Takes the last 1000 songs from Listenbrainz and scrobbles it on Libre.fm"""
import os

import pylast
import pylistenbrainz
from dotenv import load_dotenv

load_dotenv()

# Set up the LibreFM client
libre_fm = pylast.LibreFMNetwork(
    api_key="Max-----------------------------",  # This can be anything
    api_secret=os.getenv("LIBRE_FM_PASSWORD"),
    username=os.getenv("LIBRE_FM_USERNAME"),
    password_hash=pylast.md5(os.getenv("LIBRE_FM_PASSWORD")),
)

# Authenticate with Listenbrainz
listenbrainz = pylistenbrainz.ListenBrainz()
listenbrainz.set_auth_token(os.getenv("LISTENBRAINZ_AUTH_TOKEN"))

# Get last 1000 listens - scrobbling the same thing multiple times has no effect
listens = listenbrainz.get_listens("aspiringmax", count=1000)

# Populate the tracks
scrobbles = []
for listen in listens:
    data = {
        "artist": listen.artist_name,
        "title": listen.track_name,
        "timestamp": listen.listened_at,
        "album": listen.release_name,
    }
    if "tracknumber" in listen.additional_info:
        data["track_number"] = listen.additional_info["tracknumber"]
    if "duration_ms" in listen.additional_info:
        data["duration"] = listen.additional_info["duration_ms"]
    scrobbles.append(data)

# Scrobble
libre_fm.scrobble_many(scrobbles)
