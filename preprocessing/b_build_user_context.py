import json
from xml.dom import minidom
from xml.sax.saxutils import escape

def escape_text(value):
    """
    Converts the value to a string and escapes XML special characters.
    """
    return escape(str(value)) if value is not None else ''

def json_to_xml(json_data):
    """
    Converts JSON data to XML DOM object.
    """
    doc = minidom.Document()
    root = doc.createElement("articles")
    doc.appendChild(root)

    for article_id, article_data in json_data.items():
        article_elem = doc.createElement("article")
        article_elem.setAttribute("id", str(article_id))
        root.appendChild(article_elem)

        for key in ['article_title', 'article_publish_date', 'article_channel', 'article_ressort_name']:
            elem = doc.createElement(key.replace('article_', ''))
            elem.appendChild(doc.createTextNode(escape_text(article_data.get(key, ''))))
            article_elem.appendChild(elem)

        for key in ['total_comments', 'root_comments']:
            elem = doc.createElement(key)
            elem.appendChild(doc.createTextNode(str(article_data.get(key, ''))))
            article_elem.appendChild(elem)

        user_threads_elem = doc.createElement("user_threads")
        article_elem.appendChild(user_threads_elem)

        for thread in article_data['user_threads']:
            thread_elem = doc.createElement("thread")
            thread_elem.setAttribute("id", str(thread['id']))
            user_threads_elem.appendChild(thread_elem)

            for key in ['user_name', 'user_gender', 'user_created_at', 'comment_headline', 'comment_text', 'comment_created_at']:
                if key in thread:
                    elem = doc.createElement(key)
                    elem.appendChild(doc.createTextNode(escape_text(thread[key])))
                    thread_elem.appendChild(elem)

            elem = doc.createElement("comment_length")
            elem.appendChild(doc.createTextNode(str(thread['comment_length'])))
            thread_elem.appendChild(elem)

            replies_elem = doc.createElement("replies")
            thread_elem.appendChild(replies_elem)

            for reply in thread.get('replies', []):
                reply_elem = doc.createElement("reply")
                reply_elem.setAttribute("id", str(reply['id']))
                replies_elem.appendChild(reply_elem)

                for key in ['user_id', 'user_name', 'user_gender', 'user_created_at', 'comment_headline', 'comment_text', 'comment_created_at']:
                    if key in reply:
                        elem = doc.createElement(key)
                        elem.appendChild(doc.createTextNode(escape_text(reply[key])))
                        reply_elem.appendChild(elem)

                elem = doc.createElement("comment_length")
                elem.appendChild(doc.createTextNode(str(reply['comment_length'])))
                reply_elem.appendChild(elem)

    return doc

def generate_full_markdown(json_data, target_user_id):
    """
    Generates a full Markdown string from the given JSON data.
    """
    output = []

    # Find the user information for the target user_id
    user_name = None
    for article_data in json_data.values():
        for thread in article_data['user_threads']:
            if str(thread.get('user_id')) == str(target_user_id):
                user_name = thread['user_name']
                break
        if user_name:
            break

    if not user_name:
        print(f"Warning: Could not find user_name for user_id {target_user_id}")
        user_name = f"Unknown (ID: {target_user_id})"

    output.append(f"# User: {user_name} (ID: {target_user_id})\n\n")
    output.append("This document contains the thread data for the above user across multiple articles.\n\n")
    output.append("---\n\n")

    for article_id, article_data in json_data.items():
        output.append(f"## Article ID: {article_id}\n")
        output.append(f"- **Title:** {escape_text(article_data['article_title'])}\n")
        output.append(f"- **Publish Date:** {article_data['article_publish_date']}\n")
        output.append(f"- **Channel:** {escape_text(article_data['article_channel'])}\n")
        output.append(f"- **Ressort Name:** {escape_text(article_data['article_ressort_name'])}\n")
        output.append(f"- **Total Comments:** {article_data['total_comments']}\n")
        output.append(f"- **Root Comments:** {article_data['root_comments']}\n")
        output.append("\n---\n\n")

        xml_doc = json_to_xml({article_id: article_data})
        xml_content = xml_doc.toprettyxml(indent="  ")
        xml_content = '\n'.join([line for line in xml_content.split('\n') if line.strip()])
        output.append("```xml\n")
        output.append(xml_content)
        output.append("\n```\n")

    return "".join(output)

def json_to_modified_xml(json_data):
    """
    Converts JSON data to a simplified XML DOM object with selected information.
    """
    doc = minidom.Document()
    root = doc.createElement("articles")
    doc.appendChild(root)

    for article_id, article_data in json_data.items():
        article_elem = doc.createElement("article")
        article_elem.setAttribute("id", str(article_id))
        root.appendChild(article_elem)

        user_threads_elem = doc.createElement("user_threads")
        article_elem.appendChild(user_threads_elem)

        for thread in article_data['user_threads']:
            thread_elem = doc.createElement("thread")
            thread_elem.setAttribute("id", str(thread['id']))
            user_threads_elem.appendChild(thread_elem)

            for key in ['user_name', 'comment_headline', 'comment_text', 'comment_created_at']:
                simple_key = 'cmnd_' + key.split('_')[-1] if key.startswith('comment_') else key
                if key in thread:
                    elem = doc.createElement(simple_key)
                    elem.appendChild(doc.createTextNode(escape_text(thread[key])))
                    thread_elem.appendChild(elem)

            elem = doc.createElement("cmnd_length")
            elem.appendChild(doc.createTextNode(str(thread['comment_length'])))
            thread_elem.appendChild(elem)

            replies_elem = doc.createElement("replies")
            thread_elem.appendChild(replies_elem)

            for reply in thread.get('replies', []):
                reply_elem = doc.createElement("reply")
                reply_elem.setAttribute("id", str(reply['id']))
                replies_elem.appendChild(reply_elem)

                for key in ['user_name', 'comment_headline', 'comment_text', 'comment_created_at']:
                    simple_key = 'cmnd_' + key.split('_')[-1] if key.startswith('comment_') else key
                    if key in reply:
                        elem = doc.createElement(simple_key)
                        elem.appendChild(doc.createTextNode(escape_text(reply[key])))
                        reply_elem.appendChild(elem)

                elem = doc.createElement("cmnd_length")
                elem.appendChild(doc.createTextNode(str(reply['comment_length'])))
                reply_elem.appendChild(elem)

    return doc

def generate_modified_markdown(json_data, target_user_id):
    """
    Generates a modified Markdown string from the given JSON data.
    """
    output = []

    # Find the user information for the target user_id
    user_name = None
    for article_data in json_data.values():
        for thread in article_data['user_threads']:
            if str(thread.get('user_id')) == str(target_user_id):
                user_name = thread['user_name']
                break
        if user_name:
            break

    if not user_name:
        print(f"Warning: Could not find user_name for user_id {target_user_id}")
        user_name = f"Unknown (ID: {target_user_id})"

    output.append(f"# User: {user_name} (ID: {target_user_id})\n\n")
    output.append("This document contains the thread data for the above user across multiple articles.\n\n")
    output.append("---\n\n")

    for article_id, article_data in json_data.items():
        output.append(f"## Article ID: {article_id}\n")
        output.append(f"- **Title:** {escape_text(article_data['article_title'])}\n")
        output.append(f"- **Publish Date:** {article_data['article_publish_date']}\n")
        output.append(f"- **Channel:** {escape_text(article_data['article_channel'])}\n")
        output.append(f"- **Ressort Name:** {escape_text(article_data['article_ressort_name'])}\n")
        output.append(f"- **Total Comments:** {article_data['total_comments']}\n")
        output.append(f"- **Root Comments:** {article_data['root_comments']}\n")
        output.append("\n---\n\n")

        xml_doc = json_to_modified_xml({article_id: article_data})
        xml_content = xml_doc.toprettyxml(indent="  ")
        xml_content = '\n'.join([line for line in xml_content.split('\n') if line.strip()])
        output.append("```xml\n")
        output.append(xml_content)
        output.append("\n```\n")

    return "".join(output)

def main(input_path, full_output_path, modified_output_path, user_id):
    """
    Main function to read JSON from input_path, generate Markdown, and write to output paths.
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    full_markdown_content = generate_full_markdown(json_data, target_user_id=user_id)
    modified_markdown_content = generate_modified_markdown(json_data, target_user_id=user_id)

    with open(full_output_path, 'w', encoding='utf-8') as f:
        f.write(full_markdown_content)

    with open(modified_output_path, 'w', encoding='utf-8') as f:
        f.write(modified_markdown_content)
"""
if __name__ == "__main__":
    user_id = 49126
    input_path = f'spheres/JSON/user_{user_id}_threads.json'
    full_output_path = f'spheres/MD/user_{user_id}_threads_full.md'
    modified_output_path = f'spheres/MD/user_{user_id}_threads_cleaned.md'
    main(input_path, full_output_path, modified_output_path, user_id)
"""
