"""
This script reads Markdown from input.md, converts it to HTML using the markdown package,
and writes the output to an HTML file in the 'output' folder. The output filename includes a
timestamp to ensure uniqueness.
"""

import os
import datetime
import markdown

def read_markdown_file(file_path):
    """
    Read the contents of a Markdown file.
    
    Args:
        file_path (str): The path to the Markdown file.
        
    Returns:
        str: The Markdown content.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def markdown_to_html(md_text):
    """
    Convert a Markdown formatted string to HTML.
    
    Args:
        md_text (str): A string containing Markdown content.
    
    Returns:
        str: The resulting HTML content.
    """
    return markdown.markdown(md_text)

def save_html(html_content, output_dir):
    """
    Save the HTML content to a file in the specified output directory.
    The filename includes a timestamp.
    
    Args:
        html_content (str): The HTML content to save.
        output_dir (str): The directory where the HTML file will be saved.
        
    Returns:
        str: The path to the saved HTML file.
    """
    # Ensure the output directory exists; if not, create it
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate a timestamp string for the filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"output_{timestamp}.html"
    output_filepath = os.path.join(output_dir, output_filename)
    
    # Write the HTML content to the file
    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_filepath

def main():
    input_filepath = "input.md"
    output_dir = "html_output"
    
    try:
        md_content = read_markdown_file(input_filepath)
    except FileNotFoundError:
        print(f"Error: {input_filepath} does not exist.")
        return
    
    # Convert Markdown to HTML
    html_content = markdown_to_html(md_content)
    
    # Save the HTML content to a file with a timestamp in the filename
    output_file = save_html(html_content, output_dir)
    print(f"HTML output saved to: {output_file}")

if __name__ == '__main__':
    main()