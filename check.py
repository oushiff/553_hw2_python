import os

filename = "fan_fei_collabFilter.py"

command_lines = ["ratings-dataset.tsv 'Kluver' 'The Fugitive' 10",
    "ratings-dataset.tsv 'Kluver' 'The Fugitive' 20",
    "ratings-dataset.tsv 'Kluver' 'Ocean's Eleven' 30",
    "ratings-dataset.tsv 'Kluver' 'Star Wars: Episode IV - A New Hope' 30",
    "ratings-dataset.tsv 'hi mom' 'Catch Me If You Can' 30",
    "ratings-dataset.tsv 'k279' 'Spider-Man 2' 30",
    "ratings-dataset.tsv 'k279' 'Star Wars: Episode V - The Empire Strikes Back' 30",
    "ratings-dataset.tsv 'k279' 'Titanic' 30",
    "ratings-dataset.tsv '04bf3522-4cac-4579-999a-bdffd4c7d22f' 'Forrest Gump' 30",
    "ratings-dataset.tsv '04bf3522-4cac-4579-999a-bdffd4c7d22f' 'Shrek' 30",
    "ratings-dataset.tsv 'What makes you think I'm not?' 'Shrek' 30",
    "ratings-dataset.tsv 'Connor M' 'Shrek 2' 30",
    "ratings-dataset.tsv 'Connor M' 'X2: X-Men United' 30",
    "ratings-dataset.tsv 'duder21' 'Titanic' 30",
    "ratings-dataset.tsv 'duder21' 'Harry Potter and the Chamber of Secrets' 30",
    "ratings-dataset.tsv 'Molly73' 'Spider-Man' 30",
    "ratings-dataset.tsv 'Molly73' 'Gladiator' 30",
    "ratings-dataset.tsv '142a1e51-8723-45d4-85b4-54b6f87b4d4f' 'The Bourne Identity' 30",
    "ratings-dataset.tsv '142a1e51-8723-45d4-85b4-54b6f87b4d4f' 'Star Wars: Episode II - Attack of the Clones' 30"]





def get_base():
    return "python " + filename + " "

for line in command_lines:
    os.system(get_base() + line + " >> output_file")
    os.system('echo "\n\n"  >> output_file')