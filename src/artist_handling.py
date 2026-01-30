
import pandas as pd
import re


# def split_artists(artist_str):
#     """
#     Splits an artist string into main artist and featured artists.
#     """

#     # Remove quotes and unify ampersands
#     artist_str = artist_str.replace('\\&', '&')
    
#     # Split by "feat", "ft.", "featuring" (case-insensitive)
#     feat_split = re.split(r'\s+(?:feat\.?|ft\.?|featuring)\s+', artist_str, flags=re.IGNORECASE)
    
#     main_artist = feat_split[0].strip()
#     featuring_artists = []
    
#     if len(feat_split) > 1:
#         # There are featured artists
#         feat_part = feat_split[1]
#         # Split further by & or comma (inside featured artists)
#         # Remove extra spaces
#         sub_artists = re.split(r'\s*(?:&|,)\s*', feat_part)
#         featuring_artists = [a.strip() for a in sub_artists if a.strip()]
    
#     return pd.Series([main_artist, featuring_artists])

def split_artists(artist_str):
    artist_str = artist_str.replace('\\&', '&')

    parts = re.split(r'\s+(?:feat\.?|ft\.?|featuring)\s+', artist_str, flags=re.IGNORECASE)

    def split_names(s):
        return [a.strip() for a in re.split(r'\s*(?:,|&)\s*', s) if a.strip()]

    main_list = split_names(parts[0])
    feat_list = split_names(parts[1]) if len(parts) > 1 else []

    # Preserve & in the displayed main_artist string
    main_artist = " & ".join(main_list) if len(main_list) > 1 else (main_list[0] if main_list else "")

    return pd.Series([main_artist, feat_list])



def split_artists_billboard(artist_str):
    artist_str = artist_str.replace('\\&', '&')

    artists = [a.strip() for a in artist_str.split(',') if a.strip()]

    main_artist = artists[0]
    feat_artists = artists[1:] if len(artists) > 1 else []

    return pd.Series([main_artist, feat_artists])