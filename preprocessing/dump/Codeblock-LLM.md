<preprocessing>
<build_base_json.py>
import pandas as pd
import numpy as np
from datetime import datetime
import pickle
import os
import json
from typing import List, Dict


# Lade die Konfigurationen
with open('config.json', 'r') as config_file:
    config = json.load(config_file)


class DataPreprocessor:
    def __init__(self, file_path: str):
        """
        Initialize the DataPreprocessor with the file path.

        Args:
            file_path (str): The path to the CSV file containing the data.
        """
        self.file_path = file_path
        self.df = None

    def process(self):
        """
        Process the data by loading it from the CSV file and applying various preprocessing steps.
        """
        self.df = pd.read_csv(self.file_path)
        self._convert_dates()
        self._handle_missing_values()
        self._convert_id_columns()
        self._create_new_features()

    def _convert_dates(self):
        """
        Convert date columns to datetime format.
        """
        date_columns = ['PostingCreatedAt', 'ArticlePublishingDate', 'UserCreatedAt']
        for col in date_columns:
            self.df[col] = pd.to_datetime(self.df[col])

    def _handle_missing_values(self):
        """
        Handle missing values in the data by filling them with appropriate values.
        """
        self.df['PostingHeadline'] = self.df['PostingHeadline'].fillna('No Headline')
        self.df['PostingComment'] = self.df['PostingComment'].fillna('No Comment')
        self.df['UserGender'] = self.df['UserGender'].fillna('Unknown')
        self.df['UserCommunityName'] = self.df['UserCommunityName'].fillna('Unknown')

    def _convert_id_columns(self):
        """
        Convert ID columns to integer type.
        """
        id_columns = ['ID_Posting', 'ID_Posting_Parent', 'ID_CommunityIdentity', 'ID_Article']
        for col in id_columns:
            self.df[col] = self.df[col].fillna(0).astype(int)

    def _create_new_features(self):
        """
        Create new features based on existing columns.
        """
        self.df['CommentLength'] = self.df['PostingComment'].str.len()
        self.df['DaysSinceUserCreation'] = (self.df['PostingCreatedAt'] - self.df['UserCreatedAt']).dt.days
        self.df['IsReply'] = self.df['ID_Posting_Parent'] != 0
        self.df['PostingHour'] = self.df['PostingCreatedAt'].dt.hour
        self.df['PostingDayOfWeek'] = self.df['PostingCreatedAt'].dt.dayofweek

    def save_preprocessed_data(self, output_path: str):
        """
        Save the preprocessed data to a pickle file.

        Args:
            output_path (str): The path where the preprocessed data will be saved.
        """
        with open(output_path, 'wb') as f:
            pickle.dump(self.df, f)
        print(f"Preprocessed data saved to {output_path}")

    @classmethod
    def load_preprocessed_data(cls, input_path: str):
        """
        Load the preprocessed data from a pickle file.

        Args:
            input_path (str): The path to the pickle file containing the preprocessed data.

        Returns:
            DataPreprocessor: An instance of DataPreprocessor with the loaded data.
        """
        with open(input_path, 'rb') as f:
            df = pickle.load(f)
        preprocessor = cls(None)
        preprocessor.df = df
        print(f"Preprocessed data loaded from {input_path}")
        return preprocessor

class CommentThreadManager:
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the CommentThreadManager with the preprocessed data.

        Args:
            df (pd.DataFrame): The preprocessed data containing comment information.
        """
        self.df = df

    def build_comment_thread(self, comments: pd.DataFrame, parent_id: int) -> List[Dict]:
        """
        Build a hierarchical structure of comments and their replies.

        Args:
            comments (pd.DataFrame): The comments data for a specific article.
            parent_id (int): The ID of the parent comment.

        Returns:
            List[Dict]: A list of dictionaries representing the comment thread.
        """
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
            'comment_created_at': reply['PostingCreatedAt'].isoformat() if pd.notnull(reply['PostingCreatedAt']) else None,
            'comment_length': int(reply['CommentLength']),
            'article_id': int(reply['ID_Article']),
            'article_publish_date': reply['ArticlePublishingDate'].isoformat() if pd.notnull(reply['ArticlePublishingDate']) else None,
            'article_title': reply['ArticleTitle'],
            'article_channel': reply['ArticleChannel'],
            'article_ressort_name': reply['ArticleRessortName'],
            'replies': self.build_comment_thread(comments, int(reply['ID_Posting']))
        } for _, reply in replies.iterrows()]

    def get_article_threads(self) -> Dict[int, Dict]:
        """
        Get the comment threads for all articles.

        Returns:
            Dict[int, Dict]: A dictionary where keys are article IDs and values are dictionaries representing the article's comment threads.
        """
        articles = {}
        for article_id, article_df in self.df.groupby('ID_Article'):
            root_comments = article_df[article_df['ID_Posting_Parent'].isnull() | (article_df['ID_Posting_Parent'] == 0)]
            threads = self.build_comment_thread(article_df, 0)
            article_meta = article_df.iloc[0]

            articles[int(article_id)] = {
                'article_id': int(article_id),
                'article_title': article_meta['ArticleTitle'],
                'article_publish_date': article_meta['ArticlePublishingDate'].isoformat() if pd.notnull(article_meta['ArticlePublishingDate']) else None,
                'article_channel': article_meta['ArticleChannel'],
                'article_ressort_name': article_meta['ArticleRessortName'],
                'total_comments': len(article_df),
                'root_comments': len(root_comments),
                'comment_threads': threads
            }
        return articles

def main():
    # Main execution
    preprocessed_pkl_path = config["input_pkl_path"]
    input_csv_path = config["input_csv_path"]
    output_path_json = config["output_path_build_json"]

    if not os.path.exists(preprocessed_pkl_path):
        print("Preprocessed data not found. Preprocessing...")
        preprocessor = DataPreprocessor(input_csv_path)
        preprocessor.process()
        preprocessor.save_preprocessed_data(preprocessed_pkl_path)
    else:
        print("Loading preprocessed data...")
        preprocessor = DataPreprocessor.load_preprocessed_data(preprocessed_pkl_path)

    thread_manager = CommentThreadManager(preprocessor.df)
    articles_with_threads = thread_manager.get_article_threads()

    # Save the comprehensive data structure to a JSON file
    
    with open(output_path_json, 'w', encoding='utf-8') as f:
        json.dump(articles_with_threads, f, indent=2)
    print(f"Comprehensive data structure saved to {output_path_json}")

if __name__ == "__main__":
    main()
</build_base_json.py>

<build_context_md.py>
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
        markdown += f"{indent}> Erstellt am {format_date(comment['comment_created_at'])}\n\n"
        
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
</build_context_md.py>

<config.json>
{
    "input_pkl_path" : "../data/preprocessed/preprocessed_data.pkl",
    "input_json_path": "./Input_Output/JSON/articles_with_threads_full_tree.json",
    "input_csv_path": "../data/raw_csv/Postings_01052019_31052019.csv",
    "output_path_build_json" : "./Input_Output/JSON/articles_with_threads.json",
    "pkl_path_input_build_context" : "../data/preprocessed/preprocessed_data.pkl",
    


    "output_folder_markdown_generation": "./Input_Output/Markdown/",
    "output_folder_samples": "../Markdown_Samples/",
    "MIN_TOKEN_COUNT": 5000,
    "MAX_TOKEN_COUNT": 10000,
    "SAMPLE_SIZE": 20
    

}
</config.json>

<validation_script.py>
import pickle
import pandas as pd
import json
from tqdm import tqdm

# Configuration loading
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

markdown_folder = config['output_folder_markdown_generation']
pkl_path = config['input_pkl_path']
json_path = config['input_json_path']

# Step 1: Load the PKL file and extract unique user names
def load_unique_user_names():
    # Load the PKL data
    with open(pkl_path, 'rb') as file:
        pkl_data = pickle.load(file)

    # Ensure the necessary column is present
    if 'UserCommunityName' not in pkl_data.columns:
        raise KeyError("The 'UserCommunityName' column is missing from the DataFrame.")

    # Get unique user names
    unique_user_names = pkl_data['UserCommunityName'].unique()
    print(f"Unique user names from PKL: {unique_user_names}")

    return unique_user_names, pkl_data

unique_user_names, pkl_data = load_unique_user_names()

# Step 2: Count how often each user name appears in the PKL file
def count_user_occurrences_in_pkl(unique_user_names, pkl_data):
    pkl_user_counts = {}

    for user_name in tqdm(unique_user_names, desc="Counting in PKL"):
        count = (pkl_data['UserCommunityName'] == user_name).sum()
        pkl_user_counts[user_name] = count

    return pkl_user_counts

pkl_user_counts = count_user_occurrences_in_pkl(unique_user_names, pkl_data)

# Step 3: Count how often each user name appears in the JSON file using recursion
def count_user_in_json(json_data, target_user_name):
    count = 0

    for article_id, article_data in json_data.items():
        count += count_user_in_threads(article_data.get('comment_threads', []), target_user_name)

    return count

def count_user_in_threads(threads, target_user_name):
    count = 0

    for thread in threads:
        # Check the current comment
        if thread['user_name'] == target_user_name:
            count += 1
        
        # Recursively search replies
        count += count_user_in_threads(thread.get('replies', []), target_user_name)

    return count

def count_user_occurrences_in_json(unique_user_names):
    # Load the JSON data
    with open(json_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    json_user_counts = {}

    # Traverse the JSON data and count occurrences using recursion
    for user_name in tqdm(unique_user_names, desc="Counting in JSON"):
        count = count_user_in_json(json_data, user_name)
        json_user_counts[user_name] = count
        print(f"User '{user_name}' appears {count} times in the JSON file.")

    return json_user_counts

json_user_counts = count_user_occurrences_in_json(unique_user_names)

# Step 4: Validate counts between PKL and JSON and provide a summary
def validate_user_name_counts(pkl_user_counts, json_user_counts):
    successful_validations = 0
    failed_validations = 0

    for user_name in pkl_user_counts.keys():
        pkl_count = pkl_user_counts.get(user_name, 0)
        json_count = json_user_counts.get(user_name, 0)

        if pkl_count == json_count:
            successful_validations += 1
        else:
            failed_validations += 1
            print(f"Discrepancy for User '{user_name}': PKL={pkl_count}, JSON={json_count}")

    print("\nValidation Summary:")
    print(f"Successful validations: {successful_validations}")
    print(f"Failed validations: {failed_validations}")

validate_user_name_counts(pkl_user_counts, json_user_counts)
</validation_script.py>

<create_sample_set.py>
import json
import os
import shutil
import glob
from tqdm import tqdm
from datetime import datetime

def create_sample_from_files():
    """
    Generates a sample set of Markdown files based on specific token count criteria,
    and stores them in a timestamped output directory.

    This function performs the following steps:
    1. Loads configuration parameters including directory paths and token count limits.
    2. Creates a new directory with a timestamp to store the sample.
    3. Collects all metadata files from the Markdown output directory.
    4. Filters files based on their token counts against specified minimum and maximum values.
    5. Copies a limited number of eligible Markdown files to the sample directory.

    The function assumes a pre-defined structure of files and metadata to facilitate sampling.

    Raises:
        Exception: If there are issues reading configuration or copying files.

    Side Effects:
        Copies files to the specified sample directory.

    Prints:
        Progress information and any issues encountered during the file operations.
    """

    # Load configuration from a JSON file
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    markdown_folder = config['output_folder_markdown_generation']
    output_sample_folder = config['output_folder_samples']
    min_token_count = config['MIN_TOKEN_COUNT']
    max_token_count = config['MAX_TOKEN_COUNT']
    sample_size = config['SAMPLE_SIZE']

    # Create a timestamped directory for the sample output
    now = datetime.now()
    timestamp = now.strftime("%y_%m_%d__%H_%M")
    
    sample_output_dir = os.path.join(
        output_sample_folder,
        f"sample_{timestamp}_size_{sample_size}_tokens_{min_token_count}_to_{max_token_count}"
    )
    print(f"Creating sample output directory: {sample_output_dir}")
    os.makedirs(sample_output_dir, exist_ok=True)

    # Gather all metadata files
    metadata_files = glob.glob(os.path.join(markdown_folder, "*_metadata.json"))
    print(f"Found {len(metadata_files)} metadata files.")
    
    # Verify files and tokens
    eligible_files = []
    for metadata_file in tqdm(metadata_files, desc="Filtering Files"):
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        token_count = metadata.get('total_tokens', 0)
        user_id = metadata['user_id']  # Ensure user_id is always initialized
        
        print(f"Checking file {metadata_file}: Token count is {token_count}")
        
        if min_token_count <= token_count <= max_token_count:
            print(f"File eligible: user_id={user_id} with token_count={token_count}")
            eligible_files.append(user_id)
        else:
            print(f"File not eligible: user_id={user_id}, token_count={token_count}, requires between {min_token_count} and {max_token_count}")
    
    # Limit results to specified sample size
    selected_files = eligible_files[:sample_size]
    print(f"Selected files for sampling: {selected_files}")

    for user_id in tqdm(selected_files, desc="Copying Files"):
        # Find Markdown file for user
        md_file_pattern = f"user_{user_id}_comments_*_tokens.md"
        md_files = glob.glob(os.path.join(markdown_folder, md_file_pattern))
        print(f"Found markdown files for user_id={user_id}: {md_files}")
        
        for md_file in md_files:
            try:
                shutil.copy(md_file, sample_output_dir)
                print(f"Copied {md_file} to {sample_output_dir}")
            except Exception as e:
                print(f"Failed to copy {md_file}: {e}")
    
    print(f"Sample generated in {sample_output_dir}")

# Example invocation of the function
create_sample_from_files()
</create_sample_set.py>

<example_output.md>
# Benutzeraktivität von AbuTembo

## Benutzerdetails
- Benutzername: AbuTembo
- Benutzer-ID: 30
- Geschlecht: m
- Konto erstellt am: 2010-03-06T14:44:53.410000

---

## Kommentare und Threads

### Vilimsky finanzierte mit Steuergeld überwiegend plagiierte Studie
- Artikel ID: 2000102732845
- Veröffentlicht am: 2019-05-08T14:00:17
- Kanal: Inland
- Ressort: Inland
- Gesamtanzahl Kommentare: 2295

#### Kommentare
> *Headline*: No Headline
AbuTembo schreibt:
> Sie haben quasi Champagner bestellt, aber ihn nicht inhaliert.
> Erstellt am 2019-05-08T14:47



### Wie hat Österreich gewählt? Das vorläufige Endergebnis
- Artikel ID: 2000103774090
- Veröffentlicht am: 2019-05-26T16:59:28
- Kanal: Inland
- Ressort: EU-Wahl 2019 in Österreich: Wahlergebnisse und -gr
- Gesamtanzahl Kommentare: 2206

#### Kommentare
> *Headline*: No Headline
AbuTembo schreibt:
> Ich sage, dass sich von der Prognose um 2300 noch ordentlich etwas ändern wird. Da werden noch Mandate wandern. Lustig, dass die Prognose schon medial als Ergebnis verkauft wird.
> Erstellt am 2019-05-26T22:07



### Brigitte Bierlein wird erste Bundeskanzlerin Österreichs
- Artikel ID: 2000104101028
- Veröffentlicht am: 2019-05-30T18:42:14
- Kanal: Inland
- Ressort: Bundespräsident
- Gesamtanzahl Kommentare: 1824

#### Kommentare
> *Headline*: No Headline
AbuTembo schreibt:
> Ich muss immer an Brazil Von Terry Gilliam denken.
> Erstellt am 2019-05-30T19:45
</example_output.md>

</preprocessing>


<LLM_Pipeline>
<data_model>
from enum import StrEnum
from pydantic import BaseModel, Field
from typing import Annotated, List

# I use : "dimensional properties" -> "Focusing on core affect (valence and arousal) might be a useful starting point, recognizing that these are dimensional properties rather than discrete categories"

class CoreAffectAnalysis(BaseModel):
    """Represents the analysis of core affect as **dimensional properties**, including valence and arousal on the theory of Lisa Feldmann Barrett.
     Use more nuanced and specific language that captures the complexity of emotion classification after Lisa Feldmann Barrett"""
    thought: Annotated[
        str,
        Field(description="Provide a detailed step by step thought process for analyzing core affect as dimensional properties, considering both valence (pleasantness) and arousal (activation). Reference specific expressions, language, and contextual factors that indicate the user's emotional state.")
    ]
    valence: Annotated[
        str,
        Field(description="Classify the valence of the user's emotional state, reflecting the degree of pleasantness or unpleasantness. ")
    ]
    arousal: Annotated[
        str,
        Field(description="Classify the arousal level of the user's emotional state, indicating the activation or energy level.")
    ]

class EmotionalAspectExtended(BaseModel):
    """Provides an in-depth analysis of the user's emotional experience, incorporating key components of the theory of
     constructed emotions by Lisa Feldmann Barrett."""
    thought: Annotated[
        str,
        Field(description="Provide a detailed thought process for analyzing the emotional aspect, considering the user's context, cognitive appraisals, conceptualization, cultural factors, predictions, and emotional dynamics. Reference specific language and expressions used by the user.")
    ]
    context: Annotated[
        str,
        Field(description="Describe situational and social contextual factors influencing the emotion, such as the topic of discussion, current events, or interactions with other users.")
    ]
    cognitive_appraisal: Annotated[
        str,
        Field(description="Explain the user's interpretations, judgments, and meaning-making processes affecting their emotional state. Consider their perspective on events discussed.")
    ]
    conceptualization: Annotated[
        str,
        Field(description="Describe how the user's conceptual knowledge, language use, and cultural background contribute to the construction of their emotion. Reference specific concepts or metaphors used.")
    ]
    cultural_influence: Annotated[
        str,
        Field(description="Note any cultural or societal norms, values, or beliefs that may shape the user's emotional experience. Consider cultural references or shared understandings.")
    ]
    predictions_and_simulations: Annotated[
        str,
        Field(description="Discuss how the user's past experiences, memories, and expectations (predictions) influence their current emotional responses. Consider references to past events or anticipated outcomes.")
    ]
    emotional_dynamics: Annotated[
        str,
        Field(description="Indicate any changes or fluctuations in emotion throughout the comments, noting shifts in valence or arousal. Describe how emotions evolve over time or in response to interactions.")
    ]
    nuanced_classification: Annotated[
        str,
        Field(description="Classify the emotional aspect based nuanced based on the thought process, context, cognitive_appraisal, conceptualization, cultural_influence, predictions_and_simulations, emotional_dynamics. Referencing contextual and theoretical insights. Use emotion labels if appropriate, acknowledging their constructed nature.")
    ]

class EmotionalBlendAnalysis(BaseModel):
    """Represents the analysis of emotional blends in the user's experience."""
    thought: Annotated[
        str,
        Field(description="Provide a detailed thought process for identifying and analyzing multiple emotions that are intertwined within the user's comments. Describe how these emotions interact and contribute to the overall emotional experience.")
    ]
    classifications: Annotated[
        List[str],
        Field(description="List the emotions identified in the blend, acknowledging their constructed nature.")
    ]

class BasicNeed(StrEnum):
    PHYSIOLOGICAL = "Physiological"
    SAFETY = "Safety"
    LOVE_BELONGING = "Love/Belonging"
    ESTEEM = "Esteem"
    SELF_ACTUALIZATION = "Self-Actualization"

class UserNeedAnalysis(BaseModel):
    """Analyzes the user's expressed needs based on psychological theories."""
    thought: Annotated[
        str,
        Field(description="Detailed thought process for analyzing the user's needs based on their comments. Consider psychological theories of motivation and needs (e.g., Maslow's Hierarchy of Needs, Self-Determination Theory). Reference specific expressions that indicate these needs.")
    ]
    basic_needs: Annotated[
        List[BasicNeed],
        Field(description="List of basic needs fulfilled or expressed in the user's comments. Select from categories such as Physiological, Safety, Love/Belonging, Esteem, and Self-Actualization.")
    ]

class EmotionAnalysisOutput(BaseModel):
    core_affect_analysis: CoreAffectAnalysis
    emotional_aspect_extended: EmotionalAspectExtended
#    emotional_blend_analysis: EmotionalBlendAnalysis
#    user_need_analysis: UserNeedAnalysis
</data_model>

<save_output_to_csv.py>
import os
from data_models import EmotionAnalysisOutput, BasicNeed
import csv

def main(emotion_analysis: EmotionAnalysisOutput, model_temperature: float, top_p: float,
         batch_id, user_id: str, run_id: str,timestamp: str, model_name,
         prompt_template_version, filename: str = "emotion_analysis.csv",
         ):
    file_exists = os.path.isfile(filename)

    # Get all possible BasicNeed values
    #all_basic_needs = [need.value for need in BasicNeed]

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=";")

        if not file_exists:
            header = [
                         "Timestamp", "Run ID", "User ID", "batch_id", "Model Name", "Prompt Template Version",
                         "Core Affect Thought", "Valence", "Arousal",
                         "Emotional Aspect Thought", "Emotional Aspect Nuanced Classification", "Context",
                         "Cognitive Appraisal", "Conceptualization", "Cultural Influence",
                         "Predictions and Simulations", "Emotional Dynamics",
                         "model_temperature", "top_p"
        #                 "Emotional Blend Thought", "Emotional Blend Classifications",
        #                 "User Need Thought"
        #             ] + all_basic_needs  # Add all basic needs as separate columns
                ]
            writer.writerow(header)

        # Prepare the basic needs flags
        #basic_needs_flags = [1 if need in emotion_analysis.user_need_analysis.basic_needs else 0 for need in all_basic_needs]

        row = [
                  timestamp, run_id,user_id, batch_id, model_name, prompt_template_version,
                  emotion_analysis.core_affect_analysis.thought,
                  emotion_analysis.core_affect_analysis.valence,
                  emotion_analysis.core_affect_analysis.arousal,
                  emotion_analysis.emotional_aspect_extended.thought,
                  emotion_analysis.emotional_aspect_extended.nuanced_classification,
                  emotion_analysis.emotional_aspect_extended.context,
                  emotion_analysis.emotional_aspect_extended.cognitive_appraisal,
                  emotion_analysis.emotional_aspect_extended.conceptualization,
                  emotion_analysis.emotional_aspect_extended.cultural_influence,
                  emotion_analysis.emotional_aspect_extended.predictions_and_simulations,
                  emotion_analysis.emotional_aspect_extended.emotional_dynamics,
            model_temperature, top_p
    #              emotion_analysis.emotional_blend_analysis.thought,
    #           ", ".join(emotion_analysis.emotional_blend_analysis.classifications),
    #          emotion_analysis.user_need_analysis.thought
    #         ] + basic_needs_flags  # Add the flags to the row
        ]
        writer.writerow(row)

    print(f"Data has been appended to {filename}")
</save_output_to_csv.py>


<main.py>
import importlib
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.utils.json_schema import dereference_refs
from model import create_llm
from save_output_to_csv import main as save_output_to_csv
from langchain_core.tracers.context import collect_runs
from uuid import UUID, uuid4
from typing import List, Dict
from datetime import datetime
from langsmith import Client
from data_models import EmotionAnalysisOutput
from langchain_core.callbacks import StdOutCallbackHandler
from langchain_core.runnables import RunnableConfig
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate



# Load environment variables
load_dotenv()

# Dynamically import the module
models = importlib.import_module("data_models")

def load_system_prompt(filename: str, folder: Path = Path(f"./prompts/{prompts_version}")) -> Dict[str, str]:
    return (folder / filename).read_text()

def load_input(filename: str, folder: Path):
    return (folder / filename).read_text()

def create_emotion_analysis_chain(model_temperature):
    queries_schema = dereference_refs(EmotionAnalysisOutput.model_json_schema())
    queries_schema.pop("$defs", None)

    prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(str(load_system_prompt("LFB_role_setting_prompt.md"))),
            AIMessagePromptTemplate.from_template(str(load_system_prompt("LFB_role_feedback_prompt.md"))),
            HumanMessagePromptTemplate.from_template(str(load_system_prompt("user_task_prompt.md")))
        ]
    ).partial(context_sphere="context_sphere")

    llm = create_llm(
        model_name=model_name,
        temperature=model_temperature,
        response_mime_type="application/json",
        response_schema=queries_schema,
        top_p=top_p
    )

    parser = PydanticOutputParser(pydantic_object=EmotionAnalysisOutput)


    return prompt | llm | parser

def process_input_files_batch(
        input_folder: Path,
        client: Client,
        model_temperature: float,
        top_p:float,
        enable_feedback: bool,
        enable_csv_output: bool,
        batch_size: int,
        max_concurrency: int
) -> None:
    emotion_analysis_chain = create_emotion_analysis_chain(model_temperature=model_temperature)
    input_files = list(input_folder.glob("*.md"))

    # Create a callback handler
    callback_handler = StdOutCallbackHandler()

    for i in range(0, len(input_files), batch_size):
        batch_files = input_files[i:i+batch_size]
        batch_inputs = []

        for file in batch_files:
            user_id = file.name.split('_')[1]
            context_sphere = load_input(file.name, folder=input_folder)
            batch_inputs.append({
                "context_sphere": context_sphere,
                "user_id": user_id
            })
        batch_id = str(uuid4())
        tag_str = "batch: " + batch_id + " , temp: " + str(model_temperature)

        config = RunnableConfig(
            callbacks=None,
            tags=["EA_Batch_"],
            metadata={"batch_id": batch_id,
                      "temperature": model_temperature,
                      "top_p":top_p,
                      "model_name": model_name,
                      "prompt_template_version": prompts_version},
            max_concurrency=max_concurrency,
            run_name="Batch Run: EA_Chain",
        )

        with collect_runs() as runs_collector:
            batch_results = emotion_analysis_chain.batch(
                batch_inputs,
                config=config
            )

        for file, result, run in zip(batch_files, batch_results, runs_collector.traced_runs):
            user_id = file.name.split('_')[1]
            print(f"Run ID: {run.id}")
            print(f"User ID: {user_id}")
            print(result)

            if enable_feedback and run.id:
                client.create_feedback(
                    run_id=run.id,
                    key="Core Valence",
                    value=result.core_affect_analysis.valence,
                    comment=result.core_affect_analysis.thought
                )
                client.create_feedback(
                    run_id=run.id,
                    key="Core Arousal",
                    value=result.core_affect_analysis.arousal,
                    comment=result.core_affect_analysis.thought
                )
                client.create_feedback(
                    run_id=run.id,
                    key="Aspect Extended",
                    value=result.emotional_aspect_extended.nuanced_classification,
                    comment=result.emotional_aspect_extended.thought
                )

            if enable_csv_output:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_output_to_csv(emotion_analysis=result,
                                   model_temperature=model_temperature,
                                   top_p=top_p,
                                   batch_id=batch_id,
                                   user_id=user_id,
                                   run_id=run.id,
                                   timestamp=timestamp,
                                   model_name=model_name,
                                   prompt_template_version=prompts_version)

if __name__ == "__main__":
    client = Client()
    input_folder = Path("./inputs/sp0")

    # Configure which optional steps to perform
    enable_feedback = True
    enable_csv_output = True
    # Metadata variables maybe to externalize?
    # model name
    # model temperature
    # batch run
    # model configuration top_n etc.
    # prompt folder v1 / v2 / v3 / ...

    prompts_version = "v3"
    model_name = "gemini-1.5-pro-002"
    top_p = 0
    model_temperature = 0
    test_set = ""

    print("---- Start of Batch processing ----")
    process_input_files_batch(
        input_folder=input_folder,
        client=client,
        model_temperature=model_temperature,
        top_p=top_p,
        enable_feedback=True,
        enable_csv_output=True,
        batch_size=1,
        max_concurrency=1
    )
</main.py>
</LLM_Pipeline>

