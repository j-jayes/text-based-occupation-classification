import json

# Open the original file
with open('data/schemas/ssyk/occupation_codes_titles_levels_with_descriptions.json', 'r') as f:
    data = json.load(f)

# Filter the data to only include level 4 entries
level_4_data = [entry for entry in data if entry['level'] == 4]

# Write the filtered data to a new file
with open('data/schemas/ssyk/occupation_codes_titles_levels_with_descriptions_4_digit.json', 'w') as f:
    json.dump(level_4_data, f, ensure_ascii=False)