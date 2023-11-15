import json

# Load the data from the input file
with open('data/labelled-data/job-tech-excerpt.json', 'r') as f:
    data = json.load(f)

# Count the number of occurrences of each (job_title, ssyk_lvl4) pair
counts = {}
for d in data:
    key = (d['job_title'], d['ssyk_lvl4'])
    counts[key] = counts.get(key, 0) + 1

# Create a new list of unique (job_title, ssyk_lvl4, n_obs) objects
unique_data = []
for key, count in counts.items():
    unique_data.append({
        'job_title': key[0],
        'ssyk_lvl4': key[1],
        'n_obs': count
    })


# Sort the unique data by ssyk_lvl4
unique_data.sort(key=lambda x: x['ssyk_lvl4'])


# Write the unique data to a new file
with open('data/labelled-data/job-tech-excerpt-unique.json', 'w') as f:
    json.dump(unique_data, f, ensure_ascii=False)