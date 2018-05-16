import os

SONG_NAMES = "../song_names"
songs_path = os.path.join(os.getcwd(), SONG_NAMES)

files = os.listdir(songs_path)

for file in files:
    if not file.endswith('.csv'):
        continue
    with open(os.path.join(songs_path, file), 'r') as fh:
        data = fh.readlines()
        for line in data[1:]:
            number, song = line.split(',', 1)



