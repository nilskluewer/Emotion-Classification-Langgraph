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
        comments_count = complete_content.count('schreibt:')  # Count the number o