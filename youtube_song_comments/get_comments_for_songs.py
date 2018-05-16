from data_parser.parse_songs import parse_songs
import os
import subprocess

SONG_DATA_FILE = "../billboard.csv"

songs_data = parse_songs(SONG_DATA_FILE)

cur_dir = os.getcwd()

start = 150
end = len(songs_data)

songs_data = songs_data[start: end]

for song_name, year, artist, _ in songs_data:
    search_term = "%s %s" % (song_name, artist)
    args = [
        'python3',
        'get_youtube_comments_by_id.py',
        '--artist', '%s' % artist,
        '--name', '%s' % song_name
    ]
    subprocess.call(args)
    # subprocess.call(['python3', 'test.py'])
