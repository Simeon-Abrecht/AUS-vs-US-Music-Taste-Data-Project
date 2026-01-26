Dataset sources: 

The following dataset is found on Kaggle as a public access dataset:

billboard_24years_lyrics_spotify.csv -> https://www.kaggle.com/datasets/suparnabiswas/billboard-hot-1002000-2023-data-with-features

The following datasets were constructed via the chatGPT prompt: "Convert the table from {insert webpage} in to a downloadable csv filewith quotation marks around the artist and song columns". As such they do not possess the same spotify API information as the Kaggle dataset. This will be rectified in the silver layer:
(NOTE: as of 25/01/2025 Spotify's API is not available, thus musicBrainz api will be used instead. This musicbrianz data will replace the kaggle data)

Billboard_Year-End_Hot_2024 -> https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_2024

Billboard_Year-End_Hot_2025 -> https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_2025