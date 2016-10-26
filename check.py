import os

filename = """fan_fei_collabFilter.py"""

command_lines = ["""ratings-dataset.tsv 'Kluver' 'The Fugitive' 10""",
    """ratings-dataset.tsv 'Kluver' 'The Fugitive' 20""",
    """ratings-dataset.tsv 'Kluver' 'The Lion King' 30""",
    """ratings-dataset.tsv 'Kluver' 'Fight Club' 30""",
    """ratings-dataset.tsv 'hi mom' 'Star Wars: Episode IV - A New Hope' 30""",
    """ratings-dataset.tsv 'k279' 'Memento' 30""",
    """ratings-dataset.tsv 'k279' 'The Patriot' 30""",
    """ratings-dataset.tsv 'k279' 'Catch Me If You Can' 30""",
    """ratings-dataset.tsv '04bf3522-4cac-4579-999a-bdffd4c7d22f' 'The Matrix' 30""",
    """ratings-dataset.tsv '04bf3522-4cac-4579-999a-bdffd4c7d22f' 'Back to the Future' 30"""]





def get_base():
    return """python """ + filename + """ """

i = 0
for line in command_lines:
    os.system('echo "'+str(i)+'\n"  >> output_file')
    os.system(get_base() + line + """ >> output_file""")
    os.system('echo "\n\n"  >> output_file')
    i += 1