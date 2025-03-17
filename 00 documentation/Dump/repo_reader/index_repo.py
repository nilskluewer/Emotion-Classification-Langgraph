import os
import re
import sys
from lxml import etree
import pathspec
import argparse

def load_ignore_files(repo_path):
    ignore_patterns = []
    
    # Load .gitignore
    gitignore_path = os.path.join(repo_path, '.gitignore')
    if os.path.isfile(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            gitignore_content = f.read().splitlines()
        ignore_patterns.extend(gitignore_content)
        print("Loaded patterns from .gitignore")
    else:
        print("No .gitignore file found.")
    
    # Load .indexignore
    indexignore_path = os.path.join(repo_path, '.indexignore')
    if os.path.isfile(indexignore_path):
        with open(indexignore_path, 'r', encoding='utf-8') as f:
            indexignore_content = f.read().splitlines()
        ignore_patterns.extend(indexignore_content)
        print("Loaded patterns from .indexignore")
    else:
        print("No .indexignore file found.")
    
    if ignore_patterns:
        spec = pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, ignore_patterns)
        return spec
    else:
        return None

def is_ignored(path, spec):
    if spec is None:
        return False
    # Convert path to use forward slashes and remove leading './' if present
    path = path.replace(os.sep, '/').lstrip('./')
    return spec.match_file(path)

def create_xml_element(tag, text=None, attrib=None):
    element = etree.Element(tag, attrib=attrib if attrib else {})
    if text:
        element.text = text
    return element

def traverse_directory(root_path, input_folders, spec, allowed_extensions, script_extensions):
    content_root = create_xml_element('Repository', attrib={'name': os.path.basename(root_path)})
    structure_root = create_xml_element('RepositoryStructure', attrib={'name': os.path.basename(root_path)})

    for input_folder in input_folders:
        abs_input_folder = os.path.join(root_path, input_folder)
        if not os.path.isdir(abs_input_folder):
            print(f"Input folder '{input_folder}' does not exist or is not a directory.", file=sys.stderr)
            continue

        for dirpath, dirnames, filenames in os.walk(abs_input_folder):
            # Compute relative path
            rel_dir = os.path.relpath(dirpath, root_path)
            rel_dir = '.' if rel_dir == '.' else rel_dir.replace(os.sep, '/')

            # Modify dirnames in-place to skip ignored folders
            dirnames[:] = [d for d in dirnames if not is_ignored(os.path.join(rel_dir, d), spec)]

            # Navigate/Create XML elements based on relative path
            parent_content = content_root
            parent_structure = structure_root
            if rel_dir != '.':
                parts = rel_dir.split('/')
                for part in parts:
                    # For content XML
                    sub_dir = parent_content.find(f"./Directory[@name='{part}']")
                    if sub_dir is None:
                        sub_dir = create_xml_element('Directory', attrib={'name': part})
                        parent_content.append(sub_dir)
                    parent_content = sub_dir

                    # For structure XML
                    struct_sub_dir = parent_structure.find(f"./Directory[@name='{part}']")
                    if struct_sub_dir is None:
                        struct_sub_dir = create_xml_element('Directory', attrib={'name': part})
                        parent_structure.append(struct_sub_dir)
                    parent_structure = struct_sub_dir

            for filename in filenames:
                rel_file_path = os.path.join(rel_dir, filename).replace(os.sep, '/')
                if is_ignored(rel_file_path, spec):
                    continue  # Skip ignored files
                _, ext = os.path.splitext(filename)
                ext = ext.lower()
                if allowed_extensions and ext not in allowed_extensions:
                    continue  # Skip files not in allowed extensions
                file_path = os.path.join(dirpath, filename)
                try:
                    # Read and clean content
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        # Clean content to remove NULL bytes or control characters
                        content = ''.join(c for c in content if c.isprintable() or c in '\n\t\r')
                except Exception as e:
                    print(f"Error reading {file_path}: {e}", file=sys.stderr)
                    content = ""

                # For content XML
                file_element = create_xml_element('File', attrib={'name': filename, 'path': rel_file_path})
                content_element = create_xml_element('Content', text=content)
                file_element.append(content_element)
                parent_content.append(file_element)

                # For structure XML
                struct_file_element = create_xml_element('File', attrib={'name': filename, 'path': rel_file_path})
                parent_structure.append(struct_file_element)

    return content_root, structure_root

def extract_todos_and_scripts(xml_root, script_extensions):
    markdown_lines = ["# Repository Documentation\n"]
    for file_elem in xml_root.findall('.//File'):
        file_name = file_elem.get('name')
        file_path = file_elem.get('path')
        content = file_elem.find('Content').text or ''
        # Extract TODOs based on file extension
        todos = []
        ext = os.path.splitext(file_name)[1].lower()
        comment_patterns = {
            '.py': r'#\s*TODO:? (.*)',
            '.js': r'//\s*TODO:? (.*)',
            '.java': r'//\s*TODO:? (.*)',
            '.sh': r'#\s*TODO:? (.*)',
            '.rb': r'#\s*TODO:? (.*)',
            '.ts': r'//\s*TODO:? (.*)',
            '.cpp': r'//\s*TODO:? (.*)',
            '.c': r'//\s*TODO:? (.*)',
            '.cs': r'//\s*TODO:? (.*)',
            '.go': r'//\s*TODO:? (.*)',
            '.html': r'<!--\s*TODO:? (.*?)-->',
            '.css': r'/\*\s*TODO:? (.*?)\*/',
            '.scss': r'/\*\s*TODO:? (.*?)\*/',
        }
        pattern = comment_patterns.get(ext)
        if pattern:
            todos = re.findall(pattern, content, re.MULTILINE)

        # Extract scripts
        if script_extensions and ext in script_extensions:
            code = content
            markdown_lines.append(f"## `{file_path}`\n")
            markdown_lines.append("```")
            markdown_lines.append(code)
            markdown_lines.append("```\n")
        if todos:
            markdown_lines.append(f"### TODOs in `{file_path}`\n")
            markdown_lines.append("<TODOs>")
            for todo in todos:
                markdown_lines.append(f"  <TODO>{todo.strip()}</TODO>")
            markdown_lines.append("</TODOs>\n")
    return '\n'.join(markdown_lines)

def main():
    parser = argparse.ArgumentParser(description='Index selected folders in the repository.')
    parser.add_argument('folders', nargs='*', help='List of folders to process (relative to repository root). If empty, defaults to all folders.')
    parser.add_argument('--xml_output', default='results/index.xml', help='Output XML file name for content.')
    parser.add_argument('--structure_output', default='results/folder_structure.xml', help='Output XML file name for folder structure.')
    parser.add_argument('--md_output', default='results/documentation.md', help='Output Markdown file name.')
    args = parser.parse_args()

    # Configuration
    allowed_extensions = [
        '.py', '.js', '.sh', '.rb', '.java', '.md', '.html', '.css', '.ts', '.cpp', '.c', '.cs', '.go'
        # Add or remove extensions based on your requirements
    ]

    script_extensions = [
        '.py', '.js', '.sh', '.rb', '.java', '.ts', '.cpp', '.c', '.cs', '.go'
        # Add or remove script extensions as needed
    ]

    # Determine repository root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_path = os.path.abspath(os.path.join(script_dir, '..'))  # One level up from repo_reader

    # Define output paths within repo_reader/results/
    xml_output = os.path.join(script_dir, args.xml_output)
    md_output = os.path.join(script_dir, args.md_output)
    structure_output = os.path.join(script_dir, args.structure_output)
    log_file = os.path.join(script_dir, 'results', 'script_log.txt')

    # Ensure the results directory exists
    results_dir = os.path.join(script_dir, 'results')
    os.makedirs(results_dir, exist_ok=True)

    # Initialize logging
    with open(log_file, 'w', encoding='utf-8') as log_f:
        log_f.write(f"Script started. Repository path: {repo_path}\n")

    try:
        print("Loading ignore files...")
        spec = load_ignore_files(repo_path)

        # Determine input folders
        if args.folders:
            input_folders = args.folders
        else:
            # If no folders specified, process all top-level directories excluding those in .gitignore/.indexignore
            top_level_dirs = [name for name in os.listdir(repo_path) if os.path.isdir(os.path.join(repo_path, name))]
            input_folders = top_level_dirs
            print(f"No specific folders provided. Defaulting to top-level folders: {', '.join(input_folders)}")

        print("Traversing directories and building XML structures...")
        content_root, structure_root = traverse_directory(repo_path, input_folders, spec, allowed_extensions, script_extensions)

        print(f"Writing content XML to `{xml_output}`...")
        tree = etree.ElementTree(content_root)
        tree.write(xml_output, pretty_print=True, xml_declaration=True, encoding='UTF-8')

        print(f"Writing folder structure XML to `{structure_output}`...")
        struct_tree = etree.ElementTree(structure_root)
        struct_tree.write(structure_output, pretty_print=True, xml_declaration=True, encoding='UTF-8')

        print("Extracting scripts and TODOs to generate Markdown documentation...")
        markdown_content = extract_todos_and_scripts(content_root, script_extensions)

        print(f"Writing Markdown to `{md_output}`...")
        with open(md_output, 'w', encoding='utf-8') as md_file:
            md_file.write(markdown_content)

        print("Process completed successfully.")

    except Exception as e:
        error_message = f"An error occurred: {e}\n"
        print(error_message, file=sys.stderr)
        with open(log_file, 'a', encoding='utf-8') as log_f:
            log_f.write(error_message)

if __name__ == "__main__":
    main()