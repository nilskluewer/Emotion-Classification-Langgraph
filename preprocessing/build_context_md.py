import json
import os
import pickle
import tiktoken
from tqdm import tqdm
from datetime import datetime
import locale
from vertexai.generative_models import (
    GenerativeModel,
)
import vertexai

def format_date(date_string):
    """Formats a date string to include only up to minutes."""
    locale.setlocale(locale.LC_TIME, 'de_AT.UTF-8')
    date_object = datetime.strptime(date_string[:16], "%Y-%m-%dT%H:%M")
    formatted_date = date_object.strftime("%-d. %B %Y, %H:%M Uhr")
    return formatted_date

def count_tokens(text):
    """Counts tokens in the given text using tiktoken."""
    encoder = tiktoken.get_encoding("cl100k_base")
    tokens = encoder.encode(text)
    return len(tokens)

# Load configurations
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

input_json_path = config['input_json_path']
output_folder = config['output_folder_markdown_generation']
pkl_path = config['pkl_path_input_build_context']
metadata = config['metadata_file']

os.makedirs(output_folder, exist_ok=True)

# Load the JSON input file
with open(input_json_path, 'r') as f:
    data = json.load(f)

def user_in_comment_or_replies(comment, user_id):
    """Checks if a user is in a comment or its replies (recursively)."""
    if comment['user_id'] == user_id:
        return True
    for reply in comment.get('replies', []):
        if user_in_comment_or_replies(reply, user_id):
            return True
    return False

def filter_comments_by_user(comments, user_id, user_id_to_anon_name, anon_user_counter, level=0):
    """Filters comments for a specific user and their replies."""
    filtered_comments = []

    for comment in comments:
        if user_in_comment_or_replies(comment, user_id):
            # Determine the anonymous user name
            if comment['user_id'] == user_id:
                anon_username = "Analyse Zielnutzer"
            else:
                if comment['user_id'] not in user_id_to_anon_name:
                    anon_name = f"User {anon_user_counter[0]}"
                    user_id_to_anon_name[comment['user_id']] = anon_name
                    anon_user_counter[0] += 1
                anon_username = user_id_to_anon_name[comment['user_id']]
            
            new_comment = {
                "user_name": anon_username,
                "comment_headline": comment['comment_headline'],
                "comment_text": comment['comment_text'],
                "comment_created_at": comment['comment_created_at'],
                "replies": filter_comments_by_user(
                    comment.get('replies', []), user_id, user_id_to_anon_name, anon_user_counter, level + 1
                )
            }
            filtered_comments.append(new_comment)

    return filtered_comments

def generate_comment_markdown(comments, level=0):
    """Generates Markdown-formatted string from nested comments."""
    markdown = ""
    blockquote = ">" * (level + 1) + " "
    newline = "  \n"

    for comment in comments:
        if level == 0:
            markdown += f"{blockquote}{comment['user_name']} schreibt:{newline}"
        else:
            markdown += f"{blockquote}{comment['user_name']} antwortet:{newline}"

        headline = comment.get('comment_headline') or "Keine Überschrift vorhanden"
        markdown += f"{blockquote}**Überschrift**: {headline}{newline}"
        markdown += f"{blockquote}**Kommentar**: {comment['comment_text']}{newline}"
        markdown += f"{blockquote}**Kommentiert am** {format_date(comment['comment_created_at'])}{newline}{newline}"

        if comment.get('replies'):
            markdown += generate_comment_markdown(comment['replies'], level + 1)

    return markdown

def create_metadata_file(user_id, user_name, user_gender, user_created_at, total_tokens, comments_extracted):
    """Creates a JSON metadata file for a user."""
    user_name = "Analyse Zielnutzer"
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

def find_user_details_in_comments(comments, target_user_id):
    """Finds user details within comments (recursively)."""
    for comment in comments:
        if comment['user_id'] == target_user_id:
            return comment['user_name'], comment['user_gender'], comment['user_created_at']
        
        user_details = find_user_details_in_comments(comment.get('replies', []), target_user_id)
        if user_details:
            return user_details
    
    return None

def process_user_comments(data, target_user_id):
    """Processes comments for a specific user, adding thread labels."""
    all_user_comments = ""
    target_user_name, target_gender, target_created_at = "Unbekannt", "Unbekannt", "Unbekannt"

    # Initialize the mapping from user_id to anonymous names
    user_id_to_anon_name = {}
    anon_user_counter = [1]  # Using a list to make it mutable in recursion
    thread_counter = 1  # Initialize thread counter

    for article_id, article in data.items():
        user_details = find_user_details_in_comments(article.get('comment_threads', []), target_user_id)
        if user_details:
            target_user_name, target_gender, target_created_at = user_details

        header = f"## Artikel: {article['article_title']}\n\n"
        header += f"- Veröffentlicht am: {format_date(article['article_publish_date'])}\n"
        header += f"- Kanal: {article['article_channel']}\n"
        header += f"- Ressort: {article['article_ressort_name']}\n"
        header += f"- Gesamtanzahl Kommentare: {article['total_comments']}\n\n"
        header += "### Kommentare\n\n"

        comments = article.get('comment_threads', [])
        user_comments = filter_comments_by_user(
            comments, target_user_id, user_id_to_anon_name, anon_user_counter
        )

        # Add thread label before generating Markdown for each thread
        if user_comments:
            all_user_comments += f"#### Thread {thread_counter}\n\n"
            body = generate_comment_markdown(user_comments)
            all_user_comments += header + body
            thread_counter += 1  # Increment thread counter

    if all_user_comments:
        target_user_name = "Analyse Zielnutzer"
        intro = f"# Context Sphere von: {target_user_name} (Anonymisiert)\n\n"
        intro += "Dies ist eine anonymisierte Übersicht der Aktivitäten des Analyse Zielnutzers im österreichischen Online-Forum „Der Standard“ vom 01.05.2019 bis 31.05.2019. Die Kommentare sind sortiert nach Artikeln – es werden nur Artikel gezeigt, bei denen der Analyse Zielnutzer kommentiert hat, während Threads ohne seinen Beitrag ausgelassen werden. \n \n"
        intro += "Meta-Details wie Veröffentlichungszeit, Kanal und Diskussionsstruktur sind enthalten. Das “>” markiert top-level Kommentare, und jede Antwort erhält einen weiteren “>”. So signalisiert „>>“, „>>>“ usw., dass es sich um direkte Antworten und weiter verschachtelte Kommentare handelt.\n\n"

        complete_content = intro + all_user_comments
        token_count = count_tokens(complete_content)
        comments_count = complete_content.count('schreibt:') 

        filename = os.path.join(
            output_folder, f"user_{target_user_id}_comments_{token_count}_tokens.md"
        )
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(complete_content)
        if metadata:
            create_metadata_file(
                target_user_id, target_user_name, target_gender, target_created_at,
                token_count, comments_count)

def process_all_users():
    """Processes all users from the .pkl file."""
    with open(pkl_path, 'rb') as file:
        user_data = pickle.load(file)
        
    if 'ID_CommunityIdentity' not in user_data.columns:
        raise KeyError("The key 'ID_CommunityIdentity' is not found in the DataFrame. Available keys: ", user_data.columns)

    user_ids = user_data['ID_CommunityIdentity'].unique()

    for user_id in tqdm(user_ids, desc="Processing Users"):
        process_user_comments(data, user_id)

# Main call
process_all_users()



"""
# %%
import json
with open('./input_output/JSON/articles_with_threads copy.json', 'r') as articles_with_threads:
    threads = json.load(articles_with_threads)
    
vertexai.init(project="rd-ri-genai-dev-2352", location="europe-west1")
gemini_model = GenerativeModel("gemini-1.5-pro-002")

# %%
model_response = gemini_model.count_tokens([f"{threads}"])

# %%
model_response
# %%
"""