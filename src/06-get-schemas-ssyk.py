import json

def extract_refined_description(text, current_entry, next_entry):
    """
    Extracts the description from the text between the current entry and the next entry more precisely.

    Args:
    text (str): The continuous text string.
    current_entry (dict): The current occupation entry with code and title.
    next_entry (dict): The next occupation entry in the sequence.

    Returns:
    str: Extracted description.
    """
    current_pattern = f"{current_entry['code']} {current_entry['title'].split()[0]}"
    next_pattern = f"{next_entry['code']} {next_entry['title'].split()[0]}" if next_entry else ''

    start_index = text.find(current_pattern)
    end_index = text.find(next_pattern, start_index) if next_pattern else len(text)

    description = text[start_index:end_index].strip()
    description = description[len(current_pattern):].strip()

    return description

def main():
    # File paths
    json_file_path = 'data/schemas/ssyk/occupation_codes_titles_levels.json'  # Update this with the path to your JSON file
    cleaned_text_file_path = './data/schemas/ssyk/ssyk_text_cleaned.txt'  # Update this with the path to your cleaned text file

    # Reading the JSON data
    with open(json_file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    # Reading the cleaned text file
    with open(cleaned_text_file_path, 'r', encoding='utf-8') as file:
        cleaned_text = file.read()

    # Preparing the text
    cleaned_text_continuous = ' '.join(cleaned_text.split())

    # Processing each entry
    updated_json_data = []
    for i, entry in enumerate(json_data):
        next_entry = json_data[i+1] if i+1 < len(json_data) else None
        description = extract_refined_description(cleaned_text_continuous, entry, next_entry)
        updated_entry = entry.copy()
        updated_entry['description'] = description
        updated_json_data.append(updated_entry)


    # Function to remove the specified text from descriptions
    def modify_descriptions(data):
        modified_data = []
        for entry in data:
            code = entry['code']
            description = entry['description']
            # Check for "Huvudgrupp [0-9]+" pattern and match with first digit of code
            if f"Huvudgrupp {code[0]}" in description:
                # Remove "Huvudgrupp [0-9]+" and any text that follows it
                description = description.split(f"Huvudgrupp {code[0]}")[0].strip()
            modified_entry = {
                "code": entry['code'],
                "title": entry['title'],
                "level": entry['level'],
                "description": description
            }
            modified_data.append(modified_entry)
        return modified_data

    # Modify the occupation descriptions
    modified_occupation_data = modify_descriptions(updated_json_data)

    # Function to further modify descriptions by removing "Yrkesområde [0-9]" and any text that follows it
    def remove_yrkesomrade(data):
        for entry in data:
            description = entry['description']
            # Find and remove "Yrkesområde [0-9]" and any text that follows
            split_desc = description.split("Yrkesområde ")
            if len(split_desc) > 1 and split_desc[1][0].isdigit():
                entry['description'] = split_desc[0].strip()
        return data

    # Apply the additional modification to the already modified data
    further_modified_data = remove_yrkesomrade(modified_occupation_data)


    # Saving the updated JSON data
    with open('data/schemas/ssyk/occupation_codes_titles_levels_with_descriptions.json', 'w', encoding='utf-8') as file:
        json.dump(modified_occupation_data, file, indent=4, ensure_ascii=False)

    print("Processing complete. Updated JSON saved as 'occupation_codes_titles_levels_with_descriptions.json'.")

if __name__ == "__main__":
    main()
