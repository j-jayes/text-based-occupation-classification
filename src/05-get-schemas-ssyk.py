import json
import re
import fitz
import re

def save_pdf_text_to_file(pdf_file_path, text_file_path):
    with fitz.open(pdf_file_path) as pdf_file:
        pdf_text = ''
        for page_num in range(34, 104):
            page = pdf_file[page_num]
            pdf_text += page.get_text()
        # Remove unwanted text
        pdf_text = re.sub(r'^Yrkesområde \d+\s+Standard för svensk yrkesklassificering \(SSYK\) \d+\s*\n\d+\s+\nStatistiska centralbyrån\s*\n', '', pdf_text)
    with open(text_file_path, 'w') as text_file:
        text_file.write(pdf_text)

# use function
pdf_file_path = './data/pdf/ssyk.pdf'
text_file_path = './data/schemas/ssyk/ssyk_text.txt'

save_pdf_text_to_file(pdf_file_path, text_file_path)


def remove_unwanted_lines(file_path, output_path):
    """
    Removes the specified lines from the file and writes the cleaned content to a new file.

    Args:
    file_path (str): Path to the input file.
    output_path (str): Path to the output file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Lines to remove
    lines_to_remove = [
        "Standard för svensk yrkesklassificering (SSYK) 2012",
        "Yrkesområde 1",
        "Statistiska centralbyrån"
    ]

    # Processed lines will be stored here
    cleaned_lines = []

    for line in lines:
        # Remove line if it matches the unwanted lines or if it's a standalone number (page number)
        if line.strip() not in lines_to_remove and not line.strip().isdigit():
            cleaned_lines.append(line)

    # Writing the cleaned content to a new file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.writelines(cleaned_lines)

# File path for the cleaned file
file_path = './data/schemas/ssyk/ssyk_text.txt'
output_file_path = './data/schemas/ssyk/ssyk_text_cleaned.txt'

# Running the function
remove_unwanted_lines(file_path, output_file_path)


