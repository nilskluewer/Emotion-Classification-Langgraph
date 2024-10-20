import json
import os
import pickle
import pandas as pd
import tiktoken
from tqdm import tqdm  # Importiere tqdm für Fortschrittsanzeige

from datetime import datetime
from dateutil import parser

def format_date(date_string):
    """
    Formats a given date string to include only up to minutes.
    Utilizes a flexible parser to handle various date formats.
    """
    return date_string[:16]

# Token-Zählfunktion definieren
def count_tokens(text):
    """
    Encodes the given text using a specific tokenization model and returns the count of tokens.
    This is useful for understanding the token consumption for text input, particularly 
    in environments where token count might affect computational resources or cost.
    """
    encoder = tiktoken.get_encoding("cl100k_base")  # Verwende das gpt2 Modell-Encoding als Beispiel
    tokens = encoder.encode(text)
    return len(tokens)

# Lade die Konfigurationen
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

input_json_path = config['input_json_path']
output_folder = config['output_folder_markdown_generation']
pkl_path = config['pkl_path_input_build_context']  # Der Pfad zur .pkl-Datei in config.json

os.makedirs(output_folder, exist_ok=True)

# Öffne und lade die JSON-Eingabedatei
with open(input_json_path, 'r') as f:
    data = json.load(f)

# Hilfsfunktion für die Überprüfung der Benutzeraktivität
def user_in_comment_or_replies(comment, user_id):
    """
    Checks if a specific user_id is either the author of a comment or any of its replies.
    This recursive function helps traverse nested comment-reply structures 
    to locate the presence of the user in any depth level of the conversation.
    """
    if comment['user_id'] == user_id:
        return True
    for reply in comment.get('replies', []):
        if user_in_comment_or_replies(reply, user_id):
            return True
    return False

# Filterfunktion, die nur relevante Kommentare behält
def filter_comments_by_user(comments, user_id, level=0):
    """
    Filters comments for a specific user and constructs a new list of comments 
    with associated details, maintaining recursive depth structure.
    It is designed to capture all comments and replies made by the user 
    and format them for Markdown conversion while retaining indentation for hierarchy visualization.
    """
    filtered_comments = []
    indent = "  " * level

    for comment in comments:
        if user_in_comment_or_replies(comment, user_id):
            new_comment = {
                "user_name": comment['user_name'],
                "comment_headline": comment['comment_headline'],
                "comment_text": comment['comment_text'],
                "comment_created_at": comment['comment_created_at'],
                "replies": filter_comments_by_user(comment.get('replies', []), user_id, level + 1)
            }
            filtered_comments.append(new_comment)

    return filtered_comments

# Funktion zur Generierung einer Markdown-Struktur
def generate_comment_markdown(comments, level=0):
    """
    Generates a Markdown formatted string from a list of comments, recursively handling replies.
    Ensures that the hierarchical structure of comments and replies is represented 
    visually through indentation, making the output user-friendly and easy to read.
    """
    markdown = ""
    indent = "  " * level

    for comment in comments:
        # Sicherstellen, dass immer eine Headline angezeigt wird
        headline = comment.get('comment_headline')
        if not headline:
            headline = "Empty Heading"

        # Füge Headline zum Markdown-Output hinzu
        markdown += f"{indent}> *Headline*: {headline}\n"
        markdown += f"{indent}{comment['user_name']} schreibt:\n"
        markdown += f"{indent}> {comment['comment_text']}\n"
        markdown += f"{indent}> *Erstellt am {format_date(comment['comment_created_at'])}*\n\n"
        
        if 'replies' in comment and comment['replies']:
            markdown += generate_comment_markdown(comment['replies'], level + 1)

    return markdown

# Funktion zur Erstellung der Metadatendatei für einen Benutzer
def create_metadata_file(user_id, user_name, user_gender, user_created_at, total_tokens, comments_extracted):
    """
    Creates a JSON metadata file for a user, encapsulating user details 
    and statistics about their commenting activity. 
    This function supports tracking user engagement and data analysis by 
    logging structured profile data and comment history.
    """
    metadata = {
        "user_id": int(user_id),
        "user_name": user_name,
        "user_gender": user_gender,
        "user_created_at": user_created_at,
        "total_tokens": int(total_tokens),
        "comments_extracted": int(comments_extracted)
    }

    metadata_filename = os.path.join(output_folder, f"user_{user_id}_metadata.json")
    with open(metadata_filename, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    print(f"Metadata file '{metadata_filename}' created.")

# Prozessiert Kommentare eines bestimmten Benutzers
def process_user_comments(data, target_user_id):
    """
    Processes comments for a designated user by finding, filtering, and 
    formatting user-specific comments and replies. Utilizes recursive 
    strategies to fully explore thread structures and collates user detail 
    and engagement information for Markdown generation.
    """
    all_user_comments = ""
    target_user_name, target_gender, target_created_at = "Unbekannt", "Unbekannt", "Unbekannt"

    for article_id, article in data.items():
        user_details = find_user_details_in_comments(article.get('comment_threads', []), target_user_id)
        if user_details:
            target_user_name, target_gender, target_created_at = user_details

        header = f"### {article['article_title']}\n"
        header += f"- Artikel ID: {article['article_id']}\n"
        header += f"- Veröffentlicht am: {article['article_publish_date']}\n"
        header += f"- Kanal: {article['article_channel']}\n"
        header += f"- Ressort: {article['article_ressort_name']}\n"
        header += f"- Gesamtanzahl Kommentare: {article['total_comments']}\n\n"
        header += "#### Kommentare\n"

        comments = article.get('comment_threads', [])
        user_comments = filter_comments_by_user(comments, target_user_id)
        body = generate_comment_markdown(user_comments)

        if body:
            all_user_comments += header + body + "\n\n"

    if all_user_comments:
        intro = f"# Benutzeraktivität von {target_user_name}\n\n"
        intro += "## Benutzerdetails\n"
        intro += f"- Benutzername: {target_user_name}\n"
        intro += f"- Benutzer-ID: {target_user_id}\n"
        intro += f"- Geschlecht: {target_gender}\n"
        intro += f"- Konto erstellt am: {target_created_at}\n\n---\n\n"
        intro += "## Kommentare und Threads\n\n"

        complete_content = intro + all_user_comments
        token_count = count_tokens(complete_content)
        comments_count = complete_content.count('schreibt:') 

        filename = os.path.join(output_folder, f"user_{target_user_id}_comments_{token_count}_tokens.md")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(complete_content)

        create_metadata_file(target_user_id, target_user_name, target_gender, target_created_at, token_count, comments_count)

def find_user_details_in_comments(comments, target_user_id):
    """
    Searches for user information within a collection of comments, 
    employing recursion to navigate nested replies. This approach 
    ensures that no matter how deeply nested the user's comments are, 
    their details are successfully extracted.
    """
    for comment in comments:
        if comment['user_id'] == target_user_id:
            return comment['user_name'], comment['user_gender'], comment['user_created_at']
        
        # Recursively search in replies
        user_details = find_user_details_in_comments(comment.get('replies', []), target_user_id)
        if user_details:
            return user_details
    
    return None

# Prozessiert alle Benutzer aus der .pkl Datei
def process_all_users():
    """
    Loads a list of user IDs from a provided .pkl file and processes 
    each user's comments and metadata. Utilizes multiprocessing and 
    progress tracking to efficiently handle and monitor large datasets 
    during user data extraction.
    """
    with open(pkl_path, 'rb') as file:
        user_data = pickle.load(file)
        
    if 'ID_CommunityIdentity' not in user_data.columns:
        raise KeyError("The key 'ID_CommunityIdentity' is not found in the DataFrame. Available keys: ", user_data.columns)

    user_ids = user_data['ID_CommunityIdentity'].unique()

    for user_id in tqdm(user_ids, desc="Processing Users"):
        process_user_comments(data, user_id)


def test_specific_user_markdown(data, user_id=518684):
    """
    Generates a Markdown file for a specific user ID to validate 
    the handling of nested comment structures and user detail extraction.
    
    Parameters:
    - data: The JSON data containing all articles and comments.
    - user_id (int): The target user ID for which to generate the Markdown document.
    """
    all_user_comments = ""
    target_user_name, target_gender, target_created_at = "Unbekannt", "Unbekannt", "Unbekannt"

    for article_id, article in data.items():
        # Attempt to extract the user's details and comments
        user_details = find_user_details_in_comments(article.get('comment_threads', []), user_id)
        if user_details:
            target_user_name, target_gender, target_created_at = user_details

        # Prepare the article header for the markdown
        header = f"### {article['article_title']}\n"
        header += f"- Artikel ID: {article['article_id']}\n"
        header += f"- Veröffentlicht am: {article['article_publish_date']}\n"
        header += f"- Kanal: {article['article_channel']}\n"
        header += f"- Ressort: {article['article_ressort_name']}\n"
        header += f"- Gesamtanzahl Kommentare: {article['total_comments']}\n\n"
        header += "#### Kommentare\n"

        comments = article.get('comment_threads', [])
        user_comments = filter_comments_by_user(comments, user_id)
        body = generate_comment_markdown(user_comments)

        if body:
            all_user_comments += header + body + "\n\n"

    if all_user_comments:
        intro = f"# Benutzeraktivität von {target_user_name}\n\n"
        intro += "## Benutzerdetails\n"
        intro += f"- Benutzername: {target_user_name}\n"
        intro += f"- Benutzer-ID: {user_id}\n"
        intro += f"- Geschlecht: {target_gender}\n"
        intro += f"- Konto erstellt am: {target_created_at}\n\n---\n\n"
        intro += "## Kommentare und Threads\n\n"

        complete_content = intro + all_user_comments
        token_count = count_tokens(complete_content)
        comments_count = complete_content.count('schreibt:')  # Count the number of comments

        filename = os.path.join(output_folder, f"user_{user_id}_test_comments_{token_count}_tokens.md")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(complete_content)

        print(f"Test Markdown file for user ID {user_id} created: {filename}")

# Example usage
#test_specific_user_markdown(data, user_id=360)
# Hauptaufruf
process_all_users()