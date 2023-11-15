import json

def extract_job_info_v3(json_line):
    """
    Extracts job title and ssyk_lvl4 from a JSON line.
    Handles missing data and errors in JSON structure.
    """
    try:
        data = json.loads(json_line)
        # Checking if the required fields are present in the JSON structure
        if "originalJobPosting" in data and "relevantOccupation" in data["originalJobPosting"] and "name" in data["originalJobPosting"]["relevantOccupation"]:
            job_title = data["originalJobPosting"]["relevantOccupation"]["name"]
        else:
            job_title = "Not Available"
        ssyk_lvl4 = data.get("ssyk_lvl4", "Not Available")
        return {"job_title": job_title, "ssyk_lvl4": ssyk_lvl4}
    except json.JSONDecodeError:
        return None
    
def remove_not_available(data):
    return [d for d in data if d['job_title'] != 'Not Available']

def process_file_v2(input_file_path, output_file_path):
    """
    Processes the input JSON file and saves the extracted data to the output file.
    """
    extracted_data = []
    with open(input_file_path, 'r') as file:
        for line in file:
            extracted_info = extract_job_info_v3(line)
            if extracted_info:
                extracted_data.append(extracted_info)
    
    extracted_data = remove_not_available(extracted_data)

    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        json.dump(extracted_data, outfile, ensure_ascii=False)

    print(f"Data extracted and saved to {output_file_path}")


# Usage
input_file = "data/raw/job-tech-excerpt.json"  # Replace with your file path
output_file = "data/labelled-data/job-tech-excerpt.json"  # Replace with your desired output file path

process_file_v2(input_file, output_file)
