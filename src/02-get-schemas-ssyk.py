import fitz  # PyMuPDF
import re
import json

# Function to clean and merge hyphenated lines
def clean_hyphenated_lines(text):
    hyphenated_word_pattern = re.compile(r'(\w+)-\s*\n(\w+)')
    return hyphenated_word_pattern.sub(r'\1\2', text)

# Function to extract text from the PDF and clean it from any unwanted lines
def extract_and_clean_text(pdf_path, start_page, end_page):
    text = ""
    with fitz.open(pdf_path) as pdf_document:
        for page_num in range(start_page - 1, end_page):
            page = pdf_document.load_page(page_num)
            page_text = page.get_text()
            page_text = re.sub(r'(\n|^)©.*|Statistiska centralbyrån.*|[\d]+( |\xa0)*Statistiska centralbyrån.*|[\d]+( |\xa0)*SCB.*|[\d]+( |\xa0)*SSYK.*', '', page_text, flags=re.I)
            text += page_text
    return clean_hyphenated_lines(text)

# Adjust the function to exclude section headers from the occupation titles
def parse_occupations(text):
    occupations = []
    lines = text.split('\n')
    
    # Initialize a variable to store the current occupation that we're building
    current_occupation = None
    
    for line in lines:
        # If the line starts with "Yrkesområde", we are starting a new section, so we reset current_occupation
        if re.match(r'^Yrkesområde', line):
            current_occupation = None
            continue

        # If the line starts with a digit and a space, it's the start of a new occupation
        if re.match(r'^\d{1,4}\s', line):
            # If there's a current occupation being built, append it to the occupations list
            if current_occupation:
                occupations.append(current_occupation)
            
            # Start a new occupation
            code = re.match(r'^\d{1,4}', line).group()
            title = line[len(code):].strip()
            current_occupation = {
                "code": code,
                "title": title,
                "level": len(code)
            }
        # If the line doesn't start with a digit and a space, it could be a continuation of the title
        elif current_occupation:
            # If the next line is not a continuation of a title or a new code, append the current line to the title
            if not re.match(r'^\d{1,4}\s', line) and not re.match(r'^Yrkesområde', line):
                current_occupation['title'] += f' {line.strip()}'
    
    # Append the last occupation if it exists
    if current_occupation:
        occupations.append(current_occupation)
    
    # Filter out non-occupation entries (headers, footers, etc.)
    occupations = [occ for occ in occupations if len(occ['code']) > 2 or occ['code'].startswith('0')]

    return occupations

# Function to parse the text and extract occupation descriptions with consideration for group headings
def parse_descriptions_with_groups(text):
    pattern = re.compile(
        r'^(\d{4})\s(.*?nivå\s\d)(.*?)(?=\n(\d{4}\s|Yrkesgrupp \d{3}\s|\Z))', 
        re.DOTALL | re.MULTILINE
    )
    descriptions = {}
    last_code = None
    for match in re.finditer(pattern, text):
        code, title, description, next_code_or_group = match.groups()
        if last_code and last_code[:2] > code[:2]:
            break
        description = re.sub(r'\s*\n\s*', ' ', description.strip())
        descriptions[code] = {
            "title": title.strip(),
            "description": description
        }
        last_code = code
    return descriptions

# Function to parse descriptions for pages that do not have 'nivå X' in the title
def parse_descriptions_without_level(text):
    pattern = re.compile(
        r'^(\d{4})\s+(.+?)(?=\n\d{4}\s|\nYrkesgrupp|\nYrkesområde|\Z)', 
        re.DOTALL | re.MULTILINE
    )
    descriptions = {}
    for match in re.finditer(pattern, text):
        code, title_description = match.groups()
        split_position = re.search(r'\.\s+|\n', title_description)
        title = title_description[:split_position.start()].strip() if split_position else title_description.strip()
        description = title_description[split_position.end():].strip() if split_position else ''
        description = re.sub(r'\s*\n\s*', ' ', description)
        descriptions[code] = {
            "title": title,
            "description": description
        }
    return descriptions

# Replace 'pdf_path' with your PDF file path
pdf_path = './data/pdf/ssyk.pdf'

# Extract and parse occupations from pages 23 to 32
occupations_text = extract_and_clean_text(pdf_path, 23, 33)
occupations = parse_occupations(occupations_text)

# Save occupations to file
with open('./data/schemas/ssyk/occupation_codes_titles_levels.json', 'w', encoding='utf-8') as f:
    json.dump(occupations, f, ensure_ascii=False)

def parse_all_information(text):
    # The pattern looks for a code, followed by a title which might include a level,
    # and then captures the description that follows until it reaches another code, a new group heading, or the end of the text.
    pattern = re.compile(
        r'^(\d{4})\s(.*?)(nivå\s\d)?(.*?)(?=\n(\d{4}\s|Yrkesgrupp \d{3}\s|\Z))', 
        re.DOTALL | re.MULTILINE
    )
    
    all_info = []
    
    for match in re.finditer(pattern, text):
        code, title, level_suffix, description, next_code_or_group = match.groups()
        # Clean title and description
        title = re.sub(r'\s+', ' ', title.strip())
        description = re.sub(r'\s*\n\s*', ' ', description.strip())
        # Determine the level based on the code
        level = len(code)
        # Construct the final dictionary
        occupation_info = {
            "code": code,
            "title": title,
            "description": description,
            "level": level
        }
        all_info.append(occupation_info)
    
    return all_info

# Function to save the data to a JSON file
def save_to_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Loop to process pages 35 to 104 and save occupations
all_occupations_info = []
for page_num in range(35, 105):
    text = extract_and_clean_text(pdf_path, page_num, page_num + 1)
    page_info = parse_all_information(text)
    all_occupations_info.extend(page_info)

# Save the occupations to a JSON file
save_to_json(all_occupations_info, './data/schemas/ssyk/occupations_pages_35_to_test.json')

