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

# Replace 'pdf_path' with your PDF file path
pdf_path = './data/pdf/ssyk.pdf'

# Extract and parse occupations from pages 23 to 32
occupations_text = extract_and_clean_text(pdf_path, 23, 33)
occupations = parse_occupations(occupations_text)

# Save occupations to file
with open('./data/schemas/ssyk/occupation_codes_titles_levels.json', 'w', encoding='utf-8') as f:
    json.dump(occupations, f, ensure_ascii=False)

