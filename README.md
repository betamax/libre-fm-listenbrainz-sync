# Libre.fm and Listenbrainz sync scripts

Contains two scripts to sync between [Listenbrainz](https://listenbrainz.org/) and [Libre.fm](https://libre.fm/). I'm currently trying out Listenbrainz as it looks promising. I had previously been unable to set up Spotify scrobbling for Libre.fm after Spotify removed in-built scrobbling. Using this you can achieve Spotify scrobbling in Libre.fm. I first used `libre_fm_to_listenbrainz.py` to populate a new Listenbrainz account with a linked Spotify account. Then I run `listenbrainz_to_libre_fm.py` on a Raspberry Pi every hour to sync the listens collected from Spotify by Listenbrainz to my Libre.fm account. I

## Installation

```shell

# Create a virtual environment and install dependencies
python3 -m venv .venv
pip install -r requirements.txt

# Copy .env.example
cp .env.example .env

# Populate the required variables
```

## Libre.fm to Listenbrainz

```shell
python libre_fm_to_listenbrainz.py
```

## Listenbrainz to Libre.fm

```shell
python listenbrainz_to_libre_fm.py
```
