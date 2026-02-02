import pandas as pd
import requests
import time
import requests

WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql"
HEADERS = {
    "User-Agent": "ChartGenreResearch/1.0 (personal research)"
}


def sparql_escape(s: str) -> str:
    """Escape text so it can safely go inside a SPARQL double-quoted string."""
    s = str(s)
    s = s.replace("\\", "\\\\")   # backslash first
    s = s.replace('"', '\\"')     # double quotes
    s = s.replace("\n", " ").replace("\r", " ")
    return s



WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql"
HEADERS = {
    "User-Agent": "SongGenreTest/1.0 (personal research)"
}


def find_wiki_genres(song, artist, verbose = False):
    song_esc = sparql_escape(song)
    artist_esc = sparql_escape(artist)
    if verbose:
        print(f"Querying Wikidata: {song} — {artist}")
    sparql = f"""
    SELECT ?genreName WHERE {{
      ?song rdfs:label "{song_esc}"@en;
            wdt:P175 ?artist;
            wdt:P136 ?genre.
      ?artist rdfs:label "{artist_esc}"@en.
      ?genre rdfs:label ?genreName.
      FILTER(LANG(?genreName) = "en")
    }}
    """

    r = requests.get(
        WIKIDATA_ENDPOINT,
        params={"format": "json", "query": sparql},
        headers=HEADERS,
        timeout=(5, 10) #5s connect, 10s read
    )
    r.raise_for_status()
    
    genres = [row["genreName"]["value"] for row in r.json()["results"]["bindings"]]

    if verbose:
        print(f"   → found: {genres}")

    return genres