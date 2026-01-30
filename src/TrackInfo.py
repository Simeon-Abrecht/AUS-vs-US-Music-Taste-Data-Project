
import pandas as pd
import requests
import time
import json
from typing import Optional, Dict
from pprint import pprint

API_KEY = "3cb8a7d2719bb8f379dd52d7c86ff3e3"
BASE = "https://ws.audioscrobbler.com/2.0/"

def get_track_info(
    api_key: str,
    artist: str,
    track: str,
    timeout: int = 30
) -> Dict[str, Optional[str]]:
    """
    Query Last.fm for track metadata and MBIDs.

    Parameters
    ----------
    api_key : str
        Your Last.fm API key.
    artist : str
        Artist name (free text).
    track : str
        Track title (free text).
    timeout : int
        Request timeout in seconds.

    Returns
    -------
    dict
        {
            "track_name": str,
            "artist_name": str,
            "track_mbid": Optional[str],
            "artist_mbid": Optional[str]
        }

    Raises
    ------
    requests.HTTPError
        If the HTTP request fails.
    KeyError
        If the response structure is unexpected.
    """

    params = {
        "method": "track.getInfo",
        "api_key": api_key,
        "artist": artist,
        "track": track,
        "autocorrect": 1,  # improves canonical matching
        "format": "json",
    }

    response = requests.get(BASE, params=params, timeout=timeout)
    response.raise_for_status()
    data = response.json()

    track_data = data["track"]
    pprint(data["track"])

    return {
        "track_mbid": track_data.get("mbid") or None,
        "artist_mbid": track_data["artist"].get("mbid") or None,
        "duration": track_data["duration"] or None, 
        "toptags": [tag["name"] for tag in track_data["toptags"]["tag"]] or None
    }



def add_track_info(df: pd.DataFrame) -> pd.DataFrame:

    """
     Add track metadata and MBIDs to a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame with columns "artist" and "song_title".
    
    """

    enriched_rows = []

    for _, row in df.iterrows():
        try:
            info = get_track_info(
                api_key=API_KEY,
                artist=row["artist"],
                track=row["song_title"]
            )
        except Exception as e:
            # Hard fail protection – don't kill the whole run
            info = {
                "track_mbid": None,
                "artist_mbid": None,
                "duration": None,
                "toptags": None,
            }

        enriched_rows.append(info)

        time.sleep(0.2)  # IMPORTANT: be nice to the API

    enriched_df = pd.DataFrame(enriched_rows)
    final_df = pd.concat([df.reset_index(drop=True), enriched_df], axis=1)

    
    return final_df

VALID_GENRES = {
    "pop", "rnb", "soul", "dance", "hip hop", "rap",
    "rock", "alternative", "indie", "electronic",
    "house", "techno", "trance", "dubstep",
    "jazz", "blues", "funk",
    "country", "folk",
    "metal", "punk",
    "reggae", "ska",
    "classical", "opera",
    "ambient", "lofi", "emo", "Hip-Hop", 
}

@staticmethod
def clean_genre_tags(tag_value):
    # Case 1: missing value (scalar NaN)
    if tag_value is None or (isinstance(tag_value, float) and pd.isna(tag_value)):
        return []

    # Case 2: JSON string
    if isinstance(tag_value, str):
        try:
            tag_list = json.loads(tag_value)
        except json.JSONDecodeError:
            return []

    # Case 3: already a list / array
    elif isinstance(tag_value, (list, tuple, set)):
        tag_list = tag_value

    else:
        return []

    cleaned = []
    for tag in tag_list:
        tag_norm = str(tag).lower().strip()
        if tag_norm in VALID_GENRES:
            cleaned.append(tag_norm)

    return cleaned
