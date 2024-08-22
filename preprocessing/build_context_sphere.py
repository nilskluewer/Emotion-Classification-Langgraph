import pandas as pd
import numpy as np
from datetime import datetime
import pickle
import tiktoken
from typing import Dict, List, Optional, Tuple
import os
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from html import escape  # Fügen Sie diesen Import hinzu

class DataPreprocessor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None

    def process(self):
        self.df = pd.read_csv(self.file_path)
        self._convert_dates()
        self._handle_missing_values()
        self._convert_id_columns()
        self._create_new_features()

    def _convert_dates(self):
        date_columns = ['PostingCreatedAt', 'ArticlePublishingDate', 'UserCreatedAt']
        for col in date_columns:
            self.df[col] = pd.to_datetime(self.df[col])

    def _handle_missing_values(self):
        self.df['PostingHeadline'] = self.df['PostingHeadline'].fillna('No Headline')
        self.df['PostingComment'] = self.df['PostingComment'].fillna('No Comment')
        self.df['UserGender'] = self.df['UserGender'].fillna('Unknown')
        self.df['UserCommunityName'] = self.df['UserCommunityName'].fillna('Unknown')

    def _convert_id_columns(self):
        id_columns = ['ID_Posting', 'ID_Posting_Parent', 'ID_CommunityIdentity', 'ID_Article']
        for col in id_columns:
            self.df[col] = self.df[col].fillna(0).astype(int)

    def _create_new_features(self):
        self.df['CommentLength'] = self.df['PostingComment'].str.len()
        self.df['DaysSinceUserCreation'] = (self.df['PostingCreatedAt'] - self.df['UserCreatedAt']).dt.days
        self.df['IsReply'] = self.df['ID_Posting_Parent'] != 0
        self.df['PostingHour'] = self.df['PostingCreatedAt'].dt.hour
        self.df['PostingDayOfWeek'] = self.df['PostingCreatedAt'].dt.dayofweek

    def save_preprocessed_data(self, output_path: str):
        with open(output_path, 'wb') as f:
            pickle.dump(self.df, f)
        print(f"Preprocessed data saved to {output_path}")

    @classmethod
    def load_preprocessed_data(cls, input_path: str):
        with open(input_path, 'rb') as f:
            df = pickle.load(f)
        preprocessor = cls(None)
        preprocessor.df = df
        print(f"Preprocessed data loaded from {input_path}")
        return preprocessor


class CommentThreadManager:
    def __init__(self, df: pd.DataFrame):
        self.article_comments = {article_id: group for article_id, group in df.groupby('ID_Article')}

    def build_comment_thread(self, comments: pd.DataFrame, parent_id: int, depth: int = 0) -> List[Dict]:
        replies = comments[comments['ID_Posting_Parent'] == parent_id]
        return [{
            'id': int(reply['ID_Posting']),
            'parent_id': int(reply['ID_Posting_Parent']) if pd.notnull(reply['ID_Posting_Parent']) else None,
            'user_id': int(reply['ID_CommunityIdentity']),
            'user_name': reply['UserCommunityName'],
            'user_gender': reply['UserGender'],
            'user_created_at': reply['UserCreatedAt'].isoformat() if pd.notnull(reply['UserCreatedAt']) else None,
            'comment_headline': reply['PostingHeadline'],
            'comment_text': reply['PostingComment'],
            'comment_created_at': reply['PostingCreatedAt'].isoformat() if pd.notnull(
                reply['PostingCreatedAt']) else None,
            'comment_length': int(reply['CommentLength']),
            'depth': depth,
            'replies': self.build_comment_thread(comments, int(reply['ID_Posting']), depth + 1)
        } for _, reply in replies.iterrows()]

    def get_article_threads(self, article_id: int) -> Optional[Dict]:
        if article_id not in self.article_comments:
            return None

        article_df = self.article_comments[article_id]
        root_comments = article_df[article_df['ID_Posting_Parent'].isnull() | (article_df['ID_Posting_Parent'] == 0)]

        threads = self.build_comment_thread(article_df, 0)
        article_meta = article_df.iloc[0]

        return {
            'article_id': int(article_id),
            'article_title': article_meta['ArticleTitle'],
            'article_publish_date': article_meta['ArticlePublishingDate'].isoformat() if pd.notnull(
                article_meta['ArticlePublishingDate']) else None,
            'article_channel': article_meta['ArticleChannel'],
            'article_ressort_name': article_meta['ArticleRessortName'],
            'total_comments': len(article_df),
            'root_comments': len(root_comments),
            'comment_threads': threads
        }

    def get_article_ids(self) -> List[int]:
        return list(self.article_comments.keys())


class UserContextSphere:
    def __init__(self, df: pd.DataFrame, thread_manager: CommentThreadManager):
        self.df = df
        self.thread_manager = thread_manager
        self.user_comments = {user_id: group for user_id, group in df.groupby('ID_CommunityIdentity')}

    def get_user_context(self, user_id: int) -> Optional[Dict]:
        if user_id not in self.user_comments:
            return None

        user_df = self.user_comments[user_id]
        total_comments = len(user_df)
        total_replies = len(user_df[user_df['ID_Posting_Parent'].notnull()])

        user_context = {
            'user_id': int(user_id),
            'user_name': user_df['UserCommunityName'].iloc[0],
            'user_gender': user_df['UserGender'].iloc[0],
            'user_created_at': user_df['UserCreatedAt'].iloc[0].isoformat(),
            'total_comments': total_comments,
            'total_replies': total_replies,
            'articles': {}
        }

        for article_id, article_comments in user_df.groupby('ID_Article'):
            article_id = int(article_id)
            article_thread = self.thread_manager.get_article_threads(article_id)

            if article_thread:
                user_context['articles'][article_id] = {
                    'article_title': article_thread['article_title'],
                    'article_publish_date': article_thread['article_publish_date'],
                    'user_comments_count': len(article_comments),
                    'user_replies_count': len(article_comments[article_comments['ID_Posting_Parent'].notnull()]),
                    'threads': [
                        self.find_thread_for_comment(article_thread['comment_threads'], int(comment['ID_Posting']))
                        for _, comment in article_comments.iterrows()]
                }

        return user_context

    def find_thread_for_comment(self, threads: List[Dict], comment_id: int) -> Optional[Dict]:
        for thread in threads:
            if thread['id'] == comment_id:
                return thread
            result = self.find_thread_for_comment(thread['replies'], comment_id)
            if result:
                return thread
        return None

    def cutoff_after_last_interaction(self, user_context: Dict, user_id: int) -> Tuple[Dict, int]:
        removed_comments = 0

        def process_thread(thread: Dict, last_interaction_time: Optional[str]) -> Tuple[
            Optional[Dict], int, Optional[str]]:
            nonlocal removed_comments
            if thread['user_id'] == user_id:
                last_interaction_time = thread['comment_created_at']

            if last_interaction_time and thread['comment_created_at'] > last_interaction_time:
                removed_comments += 1
                return None, removed_comments, last_interaction_time

            new_replies = []
            for reply in thread['replies']:
                processed_reply, removed_comments, last_interaction_time = process_thread(reply, last_interaction_time)
                if processed_reply:
                    new_replies.append(processed_reply)

            thread['replies'] = new_replies
            return thread, removed_comments, last_interaction_time

        for article_id in user_context['articles']:
            new_threads = []
            last_interaction_time = None
            for thread in user_context['articles'][article_id]['threads']:
                processed_thread, removed_comments, last_interaction_time = process_thread(thread,
                                                                                           last_interaction_time)
                if processed_thread:
                    new_threads.append(processed_thread)
            user_context['articles'][article_id]['threads'] = new_threads

        return user_context, removed_comments

    def count_tokens(self, text: str) -> int:
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens_lst = encoding.encode(text)
        return len(tokens_lst)

    def escape_markdown(self, text: str) -> str:
        """Escape Markdown syntax in the given text."""
        # Escape characters that have special meaning in Markdown
        escape_chars = ['\\', '`', '*', '_', '{', '}', '[', ']', '(', ')', '#', '+', '-', '.', '!']
        for char in escape_chars:
            text = text.replace(char, '\\' + char)

        # Replace backticks with single quotes
        text = text.replace('`', "'")

        return text

    def format_comment_thread(self, comment: Dict) -> str:
        root = ET.Element("comment_thread")
        self.add_comment_to_xml(root, comment)
        xml_str = ET.tostring(root, encoding='unicode')
        pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")
        return pretty_xml

    def add_comment_to_xml(self, parent: ET.Element, comment: Dict):
        comment_elem = ET.SubElement(parent, "comment")
        author_elem = ET.SubElement(comment_elem, "author")
        author_elem.text = self.escape_markdown(comment['user_name'])
        content_elem = ET.SubElement(comment_elem, "content")
        content_elem.text = self.escape_markdown(comment['comment_text'])
        if comment['replies']:
            replies_elem = ET.SubElement(comment_elem, "replies")
            for reply in comment['replies']:
                self.add_comment_to_xml(replies_elem, reply)

    def generate_formatted_user_context(self, user_id: int) -> str:
        user_context = self.get_user_context(user_id)
        if not user_context:
            return f"No data found for user ID {user_id}"

        output = []

        # User Context
        output.append("# User Context\n")
        output.append(f"- **User ID:** {user_context['user_id']}\n")
        output.append(f"- **Username:** {self.escape_markdown(user_context['user_name'])}\n")
        output.append(f"- **Gender:** {self.escape_markdown(user_context['user_gender'])}\n")
        output.append(f"- **Created At:** {user_context['user_created_at']}\n")
        output.append(f"- **Total Comments:** {user_context['total_comments']}\n")
        output.append(f"- **Total Replies:** {user_context['total_replies']}\n")
        output.append("\n---\n\n")

        for article_id, article_data in user_context['articles'].items():
            # Article Context
            output.append("# Article Context\n")
            output.append(f"- **Article ID:** {article_id}\n")
            output.append(f"- **Article Title:** {self.escape_markdown(article_data['article_title'])}\n")
            output.append(f"- **Article Publish Date:** {article_data['article_publish_date']}\n")
            output.append(f"- **User Comments Count:** {article_data['user_comments_count']}\n")
            output.append(f"- **User Replies Count:** {article_data['user_replies_count']}\n")
            output.append("\n---\n\n")

            # Comment Threads
            output.append("# Comment Threads\n\n")
            for i, thread in enumerate(article_data['threads'], 1):
                output.append(f"## Thread {i}\n\n")
                output.append(self.format_comment_thread(thread))
                output.append("\n---\n\n")

        output.append("# End of Context")
        return "".join(output)

    def generate_user_report_with_cutoff(self, user_id: int) -> Tuple[str, int, int]:
        user_context = self.get_user_context(user_id)
        if not user_context:
            return f"No data found for user ID {user_id}", 0, 0

        user_context, removed_comments = self.cutoff_after_last_interaction(user_context, user_id)

        report = self.generate_formatted_user_context(user_id)
        token_count = self.count_tokens(report)

        return report, token_count, removed_comments


import json
import os

# Main execution
if __name__ == "__main__":
    preprocessed_file = "../data/preprocessed/preprocessed_data.pkl"

    if not os.path.exists(preprocessed_file):
        print("Preprocessed data not found. Preprocessing...")
        preprocessor = DataPreprocessor('../data/raw_csv/Postings_01052019_31052019.csv')
        preprocessor.process()
        preprocessor.save_preprocessed_data(preprocessed_file)
    else:
        print("Loading preprocessed data...")
        preprocessor = DataPreprocessor.load_preprocessed_data(preprocessed_file)

    thread_manager = CommentThreadManager(preprocessor.df)
    user_context_sphere = UserContextSphere(preprocessor.df, thread_manager)

    # Create the spheres directories if they don't exist
    spheres_dir_no_cutoff = "spheres/no_cutoff"
    spheres_dir_cutoff = "spheres/cutoff"
    os.makedirs(spheres_dir_no_cutoff, exist_ok=True)
    os.makedirs(spheres_dir_cutoff, exist_ok=True)

    user_id = 675862  # Replace with the desired user ID

    # Generate and save context without cutoff
    user_context_sphere = UserContextSphere(preprocessor.df, thread_manager)
    formatted_context = user_context_sphere.generate_formatted_user_context(user_id)

    if formatted_context != f"No data found for user ID {user_id}":
        filename_no_cutoff = f"{spheres_dir_no_cutoff}/{user_id}.md"
        with open(filename_no_cutoff, 'w', encoding='utf-8') as f:
            f.write(formatted_context)
        print(f"User context without cutoff saved to {filename_no_cutoff}")

        # Generate and save context with cutoff
        report, token_count, removed_comments = user_context_sphere.generate_user_report_with_cutoff(user_id)

        filename_cutoff = f"{spheres_dir_cutoff}/{user_id}.md"
        with open(filename_cutoff, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"User context with cutoff saved to {filename_cutoff}")

        print(f"Token count: {token_count}")
        print(f"Removed comments: {removed_comments}")
    else:
        error_message = f"# Error\n\nNo data found for user ID {user_id}"

        # Save error message to both directories
        for dir_path in [spheres_dir_no_cutoff, spheres_dir_cutoff]:
            filename = f"{dir_path}/{user_id}_error.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(error_message)
            print(f"Error message saved to {filename}")