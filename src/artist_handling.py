
import pandas as pd
import re


def split_artists(artist_str):
    """
    Splits an artist string into main artist and featured artists.
    """

    # Remove quotes and unify ampersands
    artist_str = artist_str.replace('\\&', '&')
    
    # Split by "feat", "ft.", "featuring" (case-insensitive)
    feat_split = re.split(r'\s+(?:feat\.?|ft\.?|featuring)\s+', artist_str, flags=re.IGNORECASE)
    
    main_artist = feat_split[0].strip()
    featuring_artists = []
    
    if len(feat_split) > 1:
        # There are featured artists
        feat_part = feat_split[1]
        # Split further by & or comma (inside featured artists)
        # Remove extra spaces
        sub_artists = re.split(r'\s*(?:&|,)\s*', feat_part)
        featuring_artists = [a.strip() for a in sub_artists if a.strip()]
    
    return pd.Series([main_artist, featuring_artists])