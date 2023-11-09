import re
import fitz

# Modified function to handle hyphenated words that may be split across lines
def clean_hyphenated_lines(text):
    """
    Joins words that are hyphenated and split across two lines.
    """
    # This pattern matches a hyphen at the end of a line and captures the next line's start
    hyphenated_word_pattern = re.compile(r'(\w+)-\n(\w+)')
    # Replace the pattern with the two parts of the word joined together
    return hyphenated_word_pattern.sub(r'\1\2', text)

# Modified function to parse the text and extract occupation information
def parse_text_to_json(text):
    # Define the regex pattern to match occupation lines with or without levels
    # This pattern is adjusted to handle multi-line titles
    pattern = re.compile(r'^(\d{1,4})\s+((?:[\S\s](?!\n\d{1,4}\s))+(?:nivå\s\d)?)', re.MULTILINE)
    occupations = []
    
    # Process each line with the regex pattern
    matches = pattern.findall(text)
    for match in matches:
        code, title = match
        # Clean the title of any unwanted whitespace or hyphens
        title = re.sub(r'\s+', ' ', title.strip())
        level = len(code)
        occupation = {
            "code": code,
            "title": title,
            "level": level
        }
        occupations.append(occupation)
    
    return occupations


# Function to parse the text and extract occupation descriptions
def parse_descriptions(text):
    # The pattern looks for a code, followed by a title which might include a level,
    # and then captures the description that follows until it reaches another code or the end of the text.
    pattern = re.compile(r'^(\d{4})\s(.*?nivå\s\d)(.*?)(?=\n\d{4}\s|\Z)', re.DOTALL | re.MULTILINE)
    
    descriptions = {}
    
    for match in re.finditer(pattern, text):
        code, title, description = match.groups()
        # Clean up the description
        description = description.strip()  # Remove leading/trailing whitespace
        description = re.sub(r'\s*\n\s*', ' ', description)  # Replace newlines and surrounding whitespace with a space
        descriptions[code] = {
            "title": title.strip(),
            "description": description
        }
    
    return descriptions

# Parse descriptions from the cleaned text of page 40
occupation_descriptions = parse_descriptions(cleaned_page_text)

# For demonstration, let's take a look at the parsed description for code "1331"
occupation_descriptions.get("1331", "Description not found")

