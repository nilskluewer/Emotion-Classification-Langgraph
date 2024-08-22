import pandas as pd
import pickle
import tiktoken
from typing import Dict, List, Tuple
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from collections import defaultdict
from data_preprocessor import DataPreprocessor
import copy
import logging
import json



class CommentThreadManager:
    """
    A class for managing comment threads associated with articles.

    This class provides functionality to build and retrieve comment threads
    for articles, maintaining the hierarchical structure of comments and replies.

    Attributes:
        article_comments (dict): A dictionary mapping article IDs to their respective comments.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initialize the CommentThreadManager with a DataFrame of comments.

        Args:
            df (pd.DataFrame): A DataFrame containing comment data for multiple articles.
        """
        self.article_comments = {article_id: group for article_id, group in df.groupby('ID_Article')}

    def build_comment_thread(self, comments: pd.DataFrame, parent_id: int, depth: int = 0) -> List[Dict]:
        """
        Recursively build a comment thread starting from a given parent comment.

        Args:
            comments (pd.DataFrame): A DataFrame containing all comments for an article.
            parent_id (int): The ID of the parent comment to start building the thread from.
            depth (int, optional): The current depth of the comment in the thread hierarchy. Defaults to 0.

        Returns:
            List[Dict]: A list of dictionaries representing the comment thread, with each dictionary
                        containing comment details and a list of replies.
        """
        replies_grouped = comments.groupby('ID_Posting_Parent')

        def build_thread(pid: int, current_depth: int) -> List[Dict]:
            if pid not in replies_grouped.groups:
                return []

            return [{
                'id': int(reply['ID_Posting']),
                'parent_id': int(reply['ID_Posting_Parent']) if pd.notnull(reply['ID_Posting_Parent']) else None,
                'user_id': int(reply['ID_CommunityIdentity']),
                'user_name': reply['UserCommunityName'],
                'user_gender': reply['UserGender'],
                'user_created_at': reply['UserCreatedAt'].isoformat() if pd.notnull(reply['UserCreatedAt']) else None,
                'comment_headline': reply['PostingHeadline'],
                'comment_text': reply['PostingComment'],
                'comment_created_at': reply['PostingCreatedAt'].isoformat() if pd.notnull(reply['PostingCreatedAt']) else None,
                'comment_length': int(reply['CommentLength']),
                'depth': current_depth,
                'replies': build_thread(int(reply['ID_Posting']), current_depth + 1)
            } for _, reply in replies_grouped.get_group(pid).iterrows()]

        return build_thread(parent_id, depth)

    def get_article_threads(self, article_id: int) -> Dict:
        """
        Retrieve the comment threads for a specific article.

        Args:
            article_id (int): The ID of the article to retrieve comment threads for.

        Returns:
            Dict: A dictionary containing article metadata and its comment threads.
                  Returns None if the article ID is not found.

        The returned dictionary includes:
        - Article metadata (ID, title, publish date, channel, ressort name)
        - Total number of comments and root comments
        - A list of comment threads
        """
        if article_id not in self.article_comments:
            return None

        article_df = self.article_comments[article_id]
        root_comments = article_df[article_df['ID_Posting_Parent'].isnull() | (article_df['ID_Posting_Parent'] == 0)]

        threads = self.build_comment_thread(article_df, 0)
        article_meta = article_df.iloc[0]

        return {
            'article_id': int(article_id),
            'article_title': article_meta['ArticleTitle'],
            'article_publish_date': article_meta['ArticlePublishingDate'].isoformat() if pd.notnull(article_meta['ArticlePublishingDate']) else None,
            'article_channel': article_meta['ArticleChannel'],
            'article_ressort_name': article_meta['ArticleRessortName'],
            'total_comments': len(article_df),
            'root_comments': len(root_comments),
            'comment_threads': threads
        }


class UserContextSphere:
    """
    A class for managing and analyzing user context within comment threads.

    This class provides functionality to retrieve user-specific context information,
    including their comments and interactions across multiple articles. It also
    generates formatted reports of user activity.

    Attributes:
        df (pd.DataFrame): The DataFrame containing all comment data.
        thread_manager (CommentThreadManager): An instance of CommentThreadManager for retrieving article threads.
        user_comments (defaultdict): A dictionary mapping user IDs to their comments.
    """

    def __init__(self, df: pd.DataFrame, thread_manager: CommentThreadManager):
        """
        Initialize the UserContextSphere with comment data and a thread manager.

        Args:
            df (pd.DataFrame): The DataFrame containing all comment data.
            thread_manager (CommentThreadManager): An instance of CommentThreadManager for retrieving article threads.
        """
        self.df = df
        self.thread_manager = thread_manager
        self.user_comments = defaultdict(list)
        self._populate_user_comments()

    def _populate_user_comments(self):
        """
        Populate the user_comments dictionary with comments grouped by user ID.
        """
        for _, row in self.df.iterrows():
            self.user_comments[row['ID_CommunityIdentity']].append(row)

    def get_user_context(self, user_id: int) -> Dict:
        """
        Retrieve the context information for a specific user.

        Args:
            user_id (int): The ID of the user to retrieve context for.

        Returns:
            Dict: A dictionary containing user context information, including user details
                  and their interactions across articles. Returns None if the user is not found.
        """
        if user_id not in self.user_comments:
            return None

        user_df = pd.DataFrame(self.user_comments[user_id])
        total_interactions = len(user_df)

        user_context = {
            'user_id': int(user_id),
            'user_name': user_df['UserCommunityName'].iloc[0],
            'user_gender': user_df['UserGender'].iloc[0],
            'user_created_at': user_df['UserCreatedAt'].iloc[0].isoformat(),
            'total_interactions': total_interactions,
            'articles': {}
        }

        for article_id, article_comments in user_df.groupby('ID_Article'):
            article_id = int(article_id)
            article_thread = self.thread_manager.get_article_threads(article_id)

            if article_thread:
                user_context['articles'][article_id] = {
                    'article_title': article_thread['article_title'],
                    'article_publish_date': article_thread['article_publish_date'],
                    'threads': [self.find_thread_for_comment(article_thread['comment_threads'], int(comment['ID_Posting']))
                                for _, comment in article_comments.iterrows()]
                }

        return user_context

    def find_thread_for_comment(self, threads: List[Dict], comment_id: int) -> Dict:
        """
        Find the thread containing a specific comment.

        Args:
            threads (List[Dict]): A list of comment threads to search.
            comment_id (int): The ID of the comment to find.

        Returns:
            Dict: The thread containing the specified comment, or None if not found.
        """
        for thread in threads:
            if thread['id'] == comment_id:
                return thread
            result = self.find_thread_for_comment(thread['replies'], comment_id)
            if result:
                return thread
        return None


    def escape_markdown(self, text: str) -> str:
        """
        Escape special characters in text for Markdown formatting.

        Args:
            text (str): The text to escape.

        Returns:
            str: The input text with special Markdown characters escaped.
        """
        escape_chars = ['\\', '`', '*', '_', '{', '}', '[', ']', '(', ')', '#', '+', '-', '.', '!']
        for char in escape_chars:
            text = text.replace(char, '\\' + char)
        return text.replace('`', "'")

    def format_comment_thread(self, comment: Dict) -> str:
        """
        Format a comment thread as an XML string.

        Args:
            comment (Dict): The root comment of the thread to format.

        Returns:
            str: A formatted XML string representing the comment thread.
        """
        root = ET.Element("comment_thread")
        self.add_comment_to_xml(root, comment)
        xml_str = ET.tostring(root, encoding='unicode')
        pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")
        return pretty_xml

    def add_comment_to_xml(self, parent: ET.Element, comment: Dict):
        """
        Add a comment and its replies to an XML element.

        Args:
            parent (ET.Element): The parent XML element to add the comment to.
            comment (Dict): The comment data to add to the XML.
        """
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
        """
        Generate a formatted Markdown report of a user's context.

        Args:
            user_id (int): The ID of the user to generate the report for.

        Returns:
            str: A formatted Markdown string containing the user's context information.
        """
        user_context = self.get_user_context(user_id)
        if not user_context:
            return f"No data found for user ID {user_id}"

        output = []

        output.append("# User Context\n")
        output.append(f"- **User ID:** {user_context['user_id']}\n")
        output.append(f"- **Username:** {self.escape_markdown(user_context['user_name'])}\n")
        output.append(f"- **Gender:** {self.escape_markdown(user_context['user_gender'])}\n")
        output.append(f"- **Created At:** {user_context['user_created_at']}\n")
        output.append(f"- **Total Interactions:** {user_context['total_interactions']}\n")
        output.append("\n---\n\n")

        for article_data in user_context['articles'].values():
            output.append("# Article Context\n")
            output.append(f"- **Article Title:** {self.escape_markdown(article_data['article_title'])}\n")
            output.append(f"- **Article Publish Date:** {article_data['article_publish_date']}\n")
            output.append("\n---\n\n")

            output.append("# Comment Threads\n\n")
            for i, thread in enumerate(article_data['threads'], 1):
                output.append(f"## Thread {i}\n\n")
                output.append(self.format_comment_thread(thread))
                output.append("\n---\n\n")

        output.append("# End of Context")
        return "".join(output)

    def generate_user_report_with_cutoff(self, user_id: int, debug: bool = False) -> Tuple[str, int, int]:
        """
        Generate a user report with a cutoff applied to limit the context.

        Args:
            user_id (int): The ID of the user to generate the report for.
            debug (bool): If True, print debug information.

        Returns:
            Tuple[str, int, int]: A tuple containing the formatted report, token count,
                                  and the number of removed comments.
        """
        user_context = self.get_user_context(user_id)
        if not user_context:
            return f"No data found for user ID {user_id}", 0, 0

        original_context = copy.deepcopy(user_context)
        user_context, removed_comments = CutoffManager.cutoff_after_last_interaction(user_context, user_id, debug)

        if not CutoffManager.validate_cutoff(original_context, user_context, user_id, debug):
            logging.error(f"Cutoff validation failed for user ID {user_id}")
            if debug:
                print("Original context:")
                print(json.dumps(original_context, indent=2))
                print("\nCutoff context:")
                print(json.dumps(user_context, indent=2))
            raise ValueError("Cutoff validation failed")

        report = self.generate_formatted_user_context(user_id)
        encoding = tiktoken.get_encoding("cl100k_base")
        token_count = len(encoding.encode(report))

        return report, token_count, removed_comments

class CutoffManager:
    """
    A class for managing the cutoff of user context data based on the user's last interaction.
    """

    @staticmethod
    def cutoff_after_last_interaction(user_context: Dict, user_id: int, debug: bool = False) -> Tuple[Dict, int]:
        """
        Cuts off the user context after the last interaction of the specified user.

        Args:
            user_context (Dict): The original user context.
            user_id (int): The ID of the user whose last interaction is used as the cutoff point.
            debug (bool): If True, print debug information.

        Returns:
            Tuple[Dict, int]: A tuple containing the modified user context and the number of removed comments.
        """
        removed_comments = 0
        last_interaction_time = None

        def process_thread(thread: Dict) -> Tuple[Dict, int]:
            nonlocal removed_comments, last_interaction_time
            if thread is None or 'comment_created_at' not in thread:
                return None, 1

            thread_time = pd.to_datetime(thread['comment_created_at'])
            if thread['user_id'] == user_id:
                if last_interaction_time is None or thread_time > last_interaction_time:
                    last_interaction_time = thread_time
                    if debug:
                        print(f"Updated last interaction time: {last_interaction_time}")

            if last_interaction_time and thread_time > last_interaction_time:
                return None, 1

            new_replies = []
            for reply in thread.get('replies', []):
                processed_reply, removed_count = process_thread(reply)
                removed_comments += removed_count
                if processed_reply:
                    new_replies.append(processed_reply)

            thread['replies'] = new_replies
            return thread, 0

        for article_id in list(user_context['articles'].keys()):
            new_threads = []
            for thread in user_context['articles'][article_id]['threads']:
                processed_thread, _ = process_thread(thread)
                if processed_thread:
                    new_threads.append(processed_thread)
                else:
                    removed_comments += 1

            user_context['articles'][article_id]['threads'] = new_threads
            if not new_threads:
                del user_context['articles'][article_id]

        if debug:
            print(f"Last interaction time: {last_interaction_time}")
            print(f"Removed comments: {removed_comments}")

        return user_context, removed_comments

    @staticmethod
    def validate_cutoff(original_context: Dict, cutoff_context: Dict, user_id: int, debug: bool = False) -> bool:
        """
        Validates the cutoff operation by comparing the original and cutoff contexts.

        Args:
            original_context (Dict): The original user context before cutoff.
            cutoff_context (Dict): The user context after cutoff.
            user_id (int): The ID of the user whose interactions are being validated.
            debug (bool): If True, print debug information.

        Returns:
            bool: True if the cutoff is valid, False otherwise.
        """
        def get_last_interaction_time(context: Dict) -> pd.Timestamp:
            last_time = None
            for article in context['articles'].values():
                for thread in article['threads']:
                    if thread['user_id'] == user_id:
                        thread_time = pd.to_datetime(thread['comment_created_at'])
                        if last_time is None or thread_time > last_time:
                            last_time = thread_time
            return last_time

        original_last_time = get_last_interaction_time(original_context)
        cutoff_last_time = get_last_interaction_time(cutoff_context)

        if debug:
            print(f"Original last interaction time: {original_last_time}")
            print(f"Cutoff last interaction time: {cutoff_last_time}")

        if original_last_time != cutoff_last_time:
            if debug:
                print("Last interaction times do not match")
            return False

        original_comment_count = 0
        cutoff_comment_count = 0

        for article_id, article in original_context['articles'].items():
            for thread in article['threads']:
                original_comment_count += 1
                thread_time = pd.to_datetime(thread['comment_created_at'])
                if thread_time <= original_last_time:
                    if article_id not in cutoff_context['articles'] or \
                            thread not in cutoff_context['articles'][article_id]['threads']:
                        if debug:
                            print(f"Missing comment in cutoff context: {thread['id']}")
                        return False

        for article_id, article in cutoff_context['articles'].items():
            for thread in article['threads']:
                cutoff_comment_count += 1
                if pd.to_datetime(thread['comment_created_at']) > original_last_time:
                    if debug:
                        print(f"Comment after last interaction time found in cutoff context: {thread['id']}")
                    return False

        if cutoff_comment_count > original_comment_count:
            if debug:
                print(f"Cutoff comment count ({cutoff_comment_count}) is greater than original comment count ({original_comment_count})")
            return False

        return True


if __name__ == "__main__":
    import os
    import pickle
    import logging

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # File paths
    preprocessed_file = "../../../data/preprocessed/preprocessed_data.pkl"
    spheres_dir_no_cutoff = "../../spheres/no_cutoff"
    spheres_dir_cutoff = "../../spheres/cutoff"

    # Create directories if they don't exist
    os.makedirs(spheres_dir_no_cutoff, exist_ok=True)
    os.makedirs(spheres_dir_cutoff, exist_ok=True)

    # Load preprocessed data
    if not os.path.exists(preprocessed_file):
        logging.error(f"Preprocessed data file not found: {preprocessed_file}")
        exit(1)

    logging.info("Loading preprocessed data...")
    with open(preprocessed_file, 'rb') as f:
        df = pickle.load(f)

    # Create instances
    thread_manager = CommentThreadManager(df)
    user_context_sphere = UserContextSphere(df, thread_manager)

    # List of user IDs to process
    user_ids = [675862, 12610, 499935]  # Add more user IDs as needed

    # Debug mode flag
    debug_mode = True

    # Process each user
    for user_id in user_ids:
        logging.info(f"Processing user ID: {user_id}")

        # Generate context without cutoff
        formatted_context = user_context_sphere.generate_formatted_user_context(user_id)
        if formatted_context != f"No data found for user ID {user_id}":
            filename_no_cutoff = f"{spheres_dir_no_cutoff}/{user_id}.md"
            with open(filename_no_cutoff, 'w', encoding='utf-8') as f:
                f.write(formatted_context)
            logging.info(f"User context without cutoff saved to {filename_no_cutoff}")

            # Generate context with cutoff
            try:
                report, token_count, removed_comments = user_context_sphere.generate_user_report_with_cutoff(user_id, debug=debug_mode)

                filename_cutoff = f"{spheres_dir_cutoff}/{user_id}.md"
                with open(filename_cutoff, 'w', encoding='utf-8') as f:
                    f.write(report)
                logging.info(f"User context with cutoff saved to {filename_cutoff}")
                logging.info(f"Token count: {token_count}")
                logging.info(f"Removed comments: {removed_comments}")

            except ValueError as e:
                logging.error(f"Error processing user {user_id} with cutoff: {str(e)}")
                error_filename = f"{spheres_dir_cutoff}/{user_id}_error.md"
                with open(error_filename, 'w', encoding='utf-8') as f:
                    f.write(f"# Error\n\n{str(e)}")
                logging.info(f"Error message saved to {error_filename}")

        else:
            logging.warning(f"No data found for user ID {user_id}")
            for dir_path in [spheres_dir_no_cutoff, spheres_dir_cutoff]:
                error_filename = f"{dir_path}/{user_id}_error.md"
                with open(error_filename, 'w', encoding='utf-8') as f:
                    f.write(f"# Error\n\nNo data found for user ID {user_id}")
                logging.info(f"Error message saved to {error_filename}")

    logging.info("Processing completed.")

