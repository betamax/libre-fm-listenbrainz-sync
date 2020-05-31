# -*- coding: utf-8 -*-
"""Takes the history from Libre.fm and adds it to Listenbrainz"""
import os
import xml.etree.ElementTree as ET

import pylistenbrainz
import requests
from dotenv import load_dotenv

load_dotenv()

URL_TEMPLATE = (
    "https://libre.fm/2.0/?method=user.getrecenttracks&api_key="
    "Max-----------------------------&user={}&page={}&limit=200"
)
LIBRE_FM_USERNAME = os.getenv("LIBRE_FM_USERNAME")

# Authenticate with Listenbrainz
listenbrainz = pylistenbrainz.ListenBrainz()
listenbrainz.set_auth_token(os.getenv("LISTENBRAINZ_AUTH_TOKEN"))


def process_page(page: int) -> None:
    """
    Takes a page number, gets the XML from libre.fm, parses it and sends to Listenbrainz
    """
    request = requests.get(URL_TEMPLATE.format(LIBRE_FM_USERNAME, page))

    xml_page = ET.fromstring(request.text)
    all_listens = xml_page.getiterator("track")  # pylint: disable=deprecated-method

    listens = []
    for listen in all_listens:
        # Iterate each listen and extract required fields
        artist_mbids = None
        if listen.find("artist") and listen.find("artist").get("mbid"):
            artist_mbids = [listen.find("artist").get("mbid")]

        listens.append(
            pylistenbrainz.Listen(
                artist_name=listen.find("artist").text,
                artist_mbids=artist_mbids,
                release_name=listen.find("album").text,
                release_mbid=listen.find("album").get("mbid"),
                track_name=listen.find("name").text,
                recording_mbid=listen.find("mbid").text,
                listened_at=listen.find("date").get("uts"),
            )
        )

    try:
        # Send all listens to Listenbrainz
        listenbrainz.submit_multiple_listens(listens)
    except pylistenbrainz.errors.ListenBrainzAPIException as exc:
        print(exc.message)
        raise exc


# Get the first page to find out how many pages there are
page_count_request = requests.get(URL_TEMPLATE.format(LIBRE_FM_USERNAME, 1))
page_count_xml = ET.fromstring(page_count_request.text)
total_pages = page_count_xml.find("recenttracks").attrib.get("totalPages")
print(f"{total_pages} pages found.")

# Iterate every page and process
for page_number in range(1, int(total_pages)):
    print(f"Processing page {page_number}")
    process_page(page_number)
