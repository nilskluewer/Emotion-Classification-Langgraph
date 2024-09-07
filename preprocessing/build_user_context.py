# Baser is -> uild_llm_readable.ipynb
import json
import os
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

def json_to_xml(json_data):
    """
    Converts JSON data to XML string.
    """
    root = ET.Element("articles")

    for article_id, article_data in json_data.items():
        article_elem = ET.SubElement(root, "article", id=str(article_id))
        ET.SubElement(article_elem, "title").text = escape(article_data['article_title'])
        ET.SubElement(article_elem, "publish_date").text = article_data['article_publish_date']
        ET.SubElement(article_elem, "channel").text = escape(article_data['article_channel'])
        ET.SubElement(article_elem, "ressort_name").text = escape(article_data['article_ressort_name'])
        ET.SubElement(article_elem, "total_comments").text = str(article_data['total_comments'])
        ET.SubElement(article_elem, "root_comments").text = str(article_data['root_comments'])

        user_threads_elem = ET.SubElement(article_elem, "user_threads")
        for thread in article_data['user_threads']:
            thread_elem = ET.SubElement(user_threads_elem, "thread", id=str(thread['id']))
            ET.SubElement(thread_elem, "user_name").text = escape(thread['user_name'])
            ET.SubElement(thread_elem, "user_name").text = escape(thread['user_name'])
            ET.SubElement(thread_elem, "user_gender").text = thread['user_gender']
            ET.SubElement(thread_elem, "user_created_at").text = thread['user_created_at']
            ET.SubElement(thread_elem, "comment_headline").text = escape(thread['comment_headline'])
            ET.SubElement(thread_elem, "comment_text").text = escape(thread['comment_text'])
            ET.SubElement(thread_elem, "comment_created_at").text = thread['comment_created_at']
            ET.SubElement(thread_elem, "comment_length").text = str(thread['comment_length'])

            replies_elem = ET.SubElement(thread_elem, "replies")
            for reply in thread['replies']:
                reply_elem = ET.SubElement(replies_elem, "reply", id=str(reply['id']))
                ET.SubElement(reply_elem, "user_id").text = str(reply['user_id'])
                ET.SubElement(reply_elem, "user_name").text = escape(reply['user_name'])
                ET.SubElement(reply_elem, "user_gender").text = reply['user_gender']
                ET.SubElement(reply_elem, "user_created_at").text = reply['user_created_at']
                ET.SubElement(reply_elem, "comment_headline").text = escape(reply['comment_headline'])
                ET.SubElement(reply_elem, "comment_text").text = escape(reply['comment_text'])
                ET.SubElement(reply_elem, "comment_created_at").text = reply['comment_created_at']
                ET.SubElement(reply_elem, "comment_length").text = str(reply['comment_length'])

    return ET.tostring(root, encoding='unicode')

def generate_full_markdown(json_data, target_user_id):
    """
    Generates a full Markdown string from the given JSON data.
    """
    output = []

    # Find the user information for the target user_id
    user_name = None
    for article_data in json_data.values():
        for thread in article_data['user_threads']:
            if str(thread['user_id']) == str(target_user_id):
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
        output.append(f"- **Title:** {article_data['article_title']}\n")
        output.append(f"- **Publish Date:** {article_data['article_publish_date']}\n")
        output.append(f"- **Channel:** {article_data['article_channel']}\n")
        output.append(f"- **Ressort Name:** {article_data['article_ressort_name']}\n")
        output.append(f"- **Total Comments:** {article_data['total_comments']}\n")
        output.append(f"- **Root Comments:** {article_data['root_comments']}\n")
        output.append("\n---\n\n")

        xml_content = json_to_xml({article_id: article_data})
        output.append("```xml\n")
        output.append(xml_content)
        output.append("\n```\n")

    return "".join(output)

def json_to_modified_xml(json_data):
    """
    Converts JSON data to a simplified XML string with selected information.
    """
    root = ET.Element("articles")

    for article_id, article_data in json_data.items():
        article_elem = ET.SubElement(root, "article", id=str(article_id))
        user_threads_elem = ET.SubElement(article_elem, "user_threads")
        for thread in article_data['user_threads']:
            thread_elem = ET.SubElement(user_threads_elem, "thread", id=str(thread['id']))
            ET.SubElement(thread_elem, "user_name").text = escape(thread['user_name'])
            ET.SubElement(thread_elem, "cmnd_headline").text = escape(thread['comment_headline'])
            ET.SubElement(thread_elem, "cmnd_text").text = escape(thread['comment_text'])
            ET.SubElement(thread_elem, "cmnd_created_at").text = thread['comment_created_at']
            ET.SubElement(thread_elem, "cmnd_length").text = str(thread['comment_length'])

            replies_elem = ET.SubElement(thread_elem, "replies")
            for reply in thread['replies']:
                reply_elem = ET.SubElement(replies_elem, "reply", id=str(reply['id']))
                ET.SubElement(reply_elem, "user_name").text = escape(reply['user_name'])
                ET.SubElement(reply_elem, "cmnd_headline").text = escape(reply['comment_headline'])
                ET.SubElement(reply_elem, "cmnd_text").text = escape(reply['comment_text'])
                ET.SubElement(reply_elem, "cmnd_created_at").text = reply['comment_created_at']
                ET.SubElement(reply_elem, "cmnd_length").text = str(reply['comment_length'])

    return ET.tostring(root, encoding='unicode')

def generate_modified_markdown(json_data, target_user_id):
    """
    Generates a modified Markdown string from the given JSON data.
    """
    output = []

    # Find the user information for the target user_id
    user_name = None
    for article_data in json_data.values():
        for thread in article_data['user_threads']:
            if str(thread['user_id']) == str(target_user_id):
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
        output.append(f"- **Title:** {article_data['article_title']}\n")
        output.append(f"- **Publish Date:** {article_data['article_publish_date']}\n")
        output.append(f"- **Channel:** {article_data['article_channel']}\n")
        output.append(f"- **Ressort Name:** {article_data['article_ressort_name']}\n")
        output.append(f"- **Total Comments:** {article_data['total_comments']}\n")
        output.append(f"- **Root Comments:** {article_data['root_comments']}\n")
        output.append("\n---\n\n")

        xml_content = json_to_modified_xml({article_id: article_data})
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


if __name__ == "__main__":
    user_id = 30537
    input_path = f'spheres/JSON/user_{user_id}_threads.json'
    full_output_path = f'spheres/MD/user_{user_id}_threads_full.md'
    modified_output_path = f'spheres/MD/user_{user_id}_threads_cleaned.md'
    main(input_path, full_output_path, modified_output_path, user_id)