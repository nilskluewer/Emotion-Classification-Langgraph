import json
from datetime import datetime
from pathlib import Path


json_data = Path
# Opening JSON file
f = open("./JSON/articles_with_threads_channel_inland.json")
 
# returns JSON object as 
# a dictionary
data = json.load(f)

def user_in_comment_or_replies(comment, user_id):
    # Check if user is the author of the comment
    if comment['user_id'] == user_id:
        return True
    # Recursively check replies
    for reply in comment.get('replies', []):
        if user_in_comment_or_replies(reply, user_id):
            return True
    return False

def filter_comments_by_user(comments, user_id, level=0):
    filtered_comments = []
    indent = "  " * level  # Two spaces per level of indentation

    for comment in comments:
        if user_in_comment_or_replies(comment, user_id):
            # Include the comment and filter its replies
            new_comment = {
                "user_name": comment['user_name'],
                "comment_text": comment['comment_text'],
                "comment_created_at": comment['comment_created_at'],
                "replies": filter_comments_by_user(comment.get('replies', []), user_id, level + 1)
            }
            filtered_comments.append(new_comment)

    return filtered_comments

def generate_markdown(comments, level=0):
    markdown = ""
    indent = "  " * level  # Two spaces per level of indentation

    for comment in comments:
        markdown += f"{indent}* **{comment['user_name']}** schreibt:\n"
        markdown += f"{indent}  - {comment['comment_text']}\n"
        markdown += f"{indent}  - *Erstellt am {comment['comment_created_at']}*\n\n"
        if 'replies' in comment and comment['replies']:
            markdown += generate_markdown(comment['replies'], level + 1)

    return markdown

def write_markdown_by_user(data, target_user_id):
    all_user_comments = ""
    
    for article_id, article in data.items():
        header = f"# {article['article_title']}\n\n"
        comments = article.get('comment_threads', [])
        
        # Filter comments based on user activity
        user_comments = filter_comments_by_user(comments, target_user_id)
        
        # Generate markdown for filtered thread
        body = generate_markdown(user_comments)
        
        # Combine header and body if body is not empty
        if body:
            all_user_comments += header + body + "\n\n"
    
    # Write all collected comments to a single markdown file
    if all_user_comments:
        filename = f"user_{target_user_id}_comments.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(all_user_comments)
        print(f"Markdown file '{filename}' created.")

# Beispiel-Aufruf
write_markdown_by_user(data, 503779)  # Ersetze 520216 mit der ID des Zielbenutzers