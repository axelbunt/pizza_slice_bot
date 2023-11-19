import json

data = []
file_to_open = 'censorship.txt'

with open(file_to_open, encoding='utf-8') as file:
    for row in file:
        row_text = row.lower().split('\n')[0]
        if row_text != '':
            data.append(row_text)

with open('censorship.json', 'w', encoding='utf-8') as file:
    json.dump(data, file)
