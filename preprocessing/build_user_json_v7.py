import json
import os

def load_json(file_path):
    """
    Load the JSON file containing articles and comments.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The loaded JSON data.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_articles_with_user_comments(articles, user_id):
    """
    Find all articles where the user has written a comment.

    Args:
        articles (dict): The dictionary containing articles and comments.
        user_id (int): The ID of the user.

    Returns:
        dict: A dictionary of articles where the user has written a comment.
    """
    user_articles = {}
    for article_id, article_data in articles.items():
        for thread in article_data['comment_threads']:
            if user_has_comment_in_thread(thread, user_id):
                user_articles[article_id] = article_data
                break
    return user_articles

def user_has_comment_in_thread(thread, user_id):
    """
    Check if the user has a comment in the given thread or its replies.

    Args:
        thread (dict): The thread to check.
        user_id (int): The ID of the user.

    Returns:
        bool: True if the user has a comment in the thread, False otherwise.
    """
    if thread['user_id'] == user_id:
        return True
    for reply in thread['replies']:
        if user_has_comment_in_thread(reply, user_id):
            return True
    return False

def find_user_threads_in_articles(articles, user_id):
    """
    Find all threads in the given articles where the user has written a comment.

    Args:
        articles (dict): The dictionary containing articles and comments.
        user_id (int): The ID of the user.

    Returns:
        dict: A dictionary of articles with threads where the user has written a comment.
    """
    user_articles = {}
    for article_id, article_data in articles.items():
        user_threads = []
        for thread in article_data['comment_threads']:
            filtered_thread = filter_thread_for_user(thread, user_id)
            if filtered_thread:
                user_threads.append(filtered_thread)

        if user_threads:
            user_articles[article_id] = {
                'article_id': article_data['article_id'],
                'article_title': article_data['article_title'],
                'article_publish_date': article_data['article_publish_date'],
                'article_channel': article_data['article_channel'],
                'article_ressort_name': article_data['article_ressort_name'],
                'total_comments': article_data['total_comments'],
                'root_comments': article_data['root_comments'],
                'user_threads': user_threads
            }

    return user_articles

def filter_thread_for_user(thread, user_id):
    """
    Filter the thread to include only the parts where the user has written a comment.

    Args:
        thread (dict): The thread to filter.
        user_id (int): The ID of the user.

    Returns:
        dict: The filtered thread, or None if the user has not written a comment in the thread.
    """
    if thread['user_id'] == user_id:
        filtered_replies = [filter_thread_for_user(reply, user_id) for reply in thread['replies']]
        filtered_replies = [reply for reply in filtered_replies if reply]
        filtered_thread = thread.copy()
        filtered_thread['replies'] = filtered_replies
        return filtered_thread
    else:
        filtered_replies = [filter_thread_for_user(reply, user_id) for reply in thread['replies']]
        filtered_replies = [reply for reply in filtered_replies if reply]
        if filtered_replies:
            filtered_thread = thread.copy()
            filtered_thread['replies'] = filtered_replies
            return filtered_thread
    return None

def save_json(data, file_path):
    """
    Save the data to a JSON file.

    Args:
        data (dict): The data to save.
        file_path (str): The path to the JSON file.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"Data saved to {file_path}")

def main(path_articles_full_tree, user_id, ):
    articles_with_threads = load_json(path_articles_full_tree)

    # Schritt 1: Finde alle Artikel, in denen der Benutzer einen Kommentar geschrieben hat
    user_articles = find_articles_with_user_comments(articles_with_threads, user_id)
    print(f"Artikel, in denen der Benutzer {user_id} einen Kommentar geschrieben hat:")
    print(json.dumps(user_articles, indent=2))

    # Schritt 2: Finde alle Threads in diesen Artikeln, in denen der Benutzer aktiv war
    user_threads_in_articles = find_user_threads_in_articles(user_articles, user_id)
    print(f"Threads, in denen der Benutzer {user_id} aktiv war:")
    print(json.dumps(user_threads_in_articles, indent=2))

    # Speichern der Ergebnisse in einer JSON-Datei
    output_dir = 'spheres/JSON'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f'user_{user_id}_threads.json')
    save_json(user_threads_in_articles, output_file)
    print("Success")