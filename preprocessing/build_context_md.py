import json
import os
import pickle
import pandas as pd
import tiktoken
from tqdm import tqdm  # Importiere tqdm für Fortschrittsanzeige

# Token-Zählfunktion definieren
def count_tokens(text):
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
    if comment['user_id'] == user_id:
        return True
    for reply in comment.get('replies', []):
        if user_in_comment_or_replies(reply, user_id):
            return True
    return False

# Filterfunktion, die nur relevante Kommentare behält
def filter_comments_by_user(comments, user_id, level=0):
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
    markdown = ""
    indent = "  " * level

    for comment in comments:
        if comment['comment_headline'] and comment['comment_headline'] != "No Headline":
            markdown += f"{indent}* **{comment['comment_headline']}**\n"
        markdown += f"{indent}  - **{comment['user_name']}** schreibt:\n"
        markdown += f"{indent}    - {comment['comment_text']}\n"
        markdown += f"{indent}    - *Erstellt am {comment['comment_created_at']}*\n\n"
        if 'replies' in comment and comment['replies']:
            markdown += generate_comment_markdown(comment['replies'], level + 1)

    return markdown

# Funktion zur Erstellung der Metadatendatei für einen Benutzer
def create_metadata_file(user_id, user_name, user_gender, user_created_at, total_tokens, comments_extracted):
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
    all_user_comments = ""
    target_user_name = "Unbekannt"
    target_gender = "Unbekannt"
    target_created_at = "Unbekannt"

    for article_id, article in data.items():
        for thread in article.get('comment_threads', []):
            if thread['user_id'] == target_user_id:
                target_user_name = thread['user_name']
                target_gender = thread['user_gender']
                target_created_at = thread['user_created_at']
                break
        
        header = f"### {article['article_title']}\n"
        header += f"- **Artikel ID**: {article['article_id']}\n"
        header += f"- **Veröffentlicht am**: {article['article_publish_date']}\n"
        header += f"- **Kanal**: {article['article_channel']}\n"
        header += f"- **Ressort**: {article['article_ressort_name']}\n"
        header += f"- **Gesamtanzahl Kommentare**: {article['total_comments']}\n\n"
        header += "#### Kommentare\n"

        comments = article.get('comment_threads', [])
        user_comments = filter_comments_by_user(comments, target_user_id)
        body = generate_comment_markdown(user_comments)

        if body:
            all_user_comments += header + body + "\n\n"

    if all_user_comments:
        intro = f"# Benutzeraktivität von {target_user_name}\n\n"
        intro += "## Benutzerdetails\n"
        intro += f"- **Benutzername**: {target_user_name}\n"
        intro += f"- **Benutzer-ID**: {target_user_id}\n"
        intro += f"- **Geschlecht**: {target_gender}\n"
        intro += f"- **Konto erstellt am**: {target_created_at}\n\n---\n\n"
        intro += "## Kommentare und Threads\n\n"

        complete_content = intro + all_user_comments
        token_count = count_tokens(complete_content)
        comments_count = complete_content.count('schreibt:')  # Kommentare zählen

        filename = os.path.join(output_folder, f"user_{target_user_id}_comments_{token_count}_tokens.md")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(complete_content)

        create_metadata_file(target_user_id, target_user_name, target_gender, target_created_at, token_count, comments_count)

# Prozessiert alle Benutzer aus der .pkl Datei
def process_all_users():
    with open(pkl_path, 'rb') as file:
        user_data = pickle.load(file)
        
    if 'ID_CommunityIdentity' not in user_data.columns:
        raise KeyError("The key 'ID_CommunityIdentity' is not found in the DataFrame. Available keys: ", user_data.columns)

    user_ids = user_data['ID_CommunityIdentity'].unique()

    for user_id in tqdm(user_ids, desc="Processing Users"):
        process_user_comments(data, user_id)

# Hauptaufruf
process_all_users()