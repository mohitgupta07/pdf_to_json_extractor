# pip install pdfminer.six beautifulsoup4

from pdfminer.high_level import extract_text
from bs4 import BeautifulSoup
import re

# Function to convert PDF text to structured HTML
def convert_pdf_to_html(pdf_path):
    # Extract text from PDF
    text = extract_text(pdf_path, codec='Identity-H')

    # Initialize BeautifulSoup HTML document
    soup = BeautifulSoup('<html><body></body></html>', 'html.parser')
    body = soup.find('body')

    # Split text into lines for processing
    lines = text.split('\n')
    for line in lines:
        # Simple logic to identify headings - can be improved
        if line.isupper():
            heading = soup.new_tag('h2')
            heading.string = line
            body.append(heading)
        else:
            paragraph = soup.new_tag('p')
            paragraph.string = line
            body.append(paragraph)

    # Return the structured HTML
    return str(soup)

# Example usage
pdf_path = '/Users/hit/Downloads/GetSafe.pdf'  # Replace with your PDF file path
html_output = convert_pdf_to_html(pdf_path)
with open("test.html", "w", encoding='utf-8') as file:
    file.write(str(html_output))
print(html_output)
