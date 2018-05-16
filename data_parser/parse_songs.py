SONG_FILE = "../billboard.csv"

def parse_songs(song_file):
    song_data = []  # List of (name, year, artist, lyrics) tuples.
    skipped = False
    with open(song_file, 'r', encoding='utf-8') as fh:
        for line in fh:
            if not skipped:
                skipped = True
                continue
            tokens = line.split(',', 4)
            _, song, year, artist, lyrics = tokens
            song_data.append((song, year, artist, lyrics))
    return song_data

if __name__ == "__main__":
    songs = parse_songs(SONG_FILE)
    for s in songs:
        print(s)