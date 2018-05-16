SONG_FILE = "../billboard.csv"

def parse_songs(song_file):
    song_data = [] # List of (name, year, artist, lyrics) tuples.
    with open(song_file, 'r') as fh:
        for line in fh:
            tokens = line.split(',', 4)
            _, song, year, artist, lyrics = tokens
            song_data.append((song, year, artist, lyrics))
    return song_data
