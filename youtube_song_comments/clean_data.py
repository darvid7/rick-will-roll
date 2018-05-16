import os
import json
from data_parser.parse_songs import parse_songs

data_files = [
    '../youtube_comments/1_youtube_comment_data.text',
    '../youtube_comments/youtube_comment_data.text'
]

SONG_DATA_FILE = "../billboard.csv"

songs_data = parse_songs(SONG_DATA_FILE)

# Keys made up of 'song name artist'

song_keys = []

for song_name, year, artist, lyrics in songs_data:
    search_term = "%s %s" % (song_name, artist)
    song_keys.append(search_term)

unique_song_keys = set(song_keys)

processed_song_keys = {}

# Uniqueify data.
for file in data_files:
    with open(os.path.join(os.getcwd(), file), 'r', encoding='utf-8') as fh:
        for line in fh:
            song_key, youtube_id, comment_list = line.split(',', 2)
            if song_key in processed_song_keys:
                continue
            comment_list = comment_list.lstrip()
            comment_list = comment_list.lstrip()
            comment_list = eval(comment_list) # Turns into list.
            print(comment_list)
            processed_song_keys[song_key] = {
                'youtube_id': youtube_id,
                'comments': comment_list
            }
with open('cleaned_youtube_comment_data.json', 'w') as fh:
    fh.write(json.dumps(processed_song_keys))