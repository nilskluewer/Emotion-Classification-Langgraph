# filter_and_sample.py

import pandas as pd
import json
import os
from typing import Dict
from build_base_json import DataPreprocessor, CommentThreadManager  # Assuming the base script is named base_script.py

def filter_users_by_comment_count(df: pd.DataFrame, min_comments: int, max_comments: int) -> pd.DataFrame:
    """
    Filter users based on the number of comments they have made.

    Args:
        df (pd.DataFrame): The preprocessed data.
        min_comments (int): Minimum number of comments a user must have made to be included.
        max_comments (int): Maximum number of comments a user can have made to be included.

    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    user_comment_counts = df['ID_CommunityIdentity'].value_counts()
    filtered_users = user_comment_counts[(user_comment_counts >= min_comments) & (user_comment_counts <= max_comments)].index
    return df[df['ID_CommunityIdentity'].isin(filtered_users)]

def sample_users(df: pd.DataFrame, num_users: int) -> pd.DataFrame:
    """
    Sample a specified number of users from the DataFrame.

    Args:
        df (pd.DataFrame): The preprocessed data.
        num_users (int): Number of users to sample.

    Returns:
        pd.DataFrame: DataFrame containing only the sampled users.
    """
    unique_users = df['ID_CommunityIdentity'].unique()
    sampled_users = np.random.choice(unique_users, size=min(num_users, len(unique_users)), replace=False)
    return df[df['ID_CommunityIdentity'].isin(sampled_users)]

def save_filtered_json(df: pd.DataFrame, output_path: str):
    """
    Save the filtered and sampled data to a JSON file.

    Args:
        df (pd.DataFrame): The filtered and sampled data.
        output_path (str): The path where the JSON data will be saved.
    """
    thread_manager = CommentThreadManager(df)
    articles_with_threads = thread_manager.get_article_threads()

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(articles_with_threads, f, indent=2)
    print(f"Filtered and sampled data saved to {output_path}")

def main():
    preprocessed_file = r"../data/preprocessed/preprocessed_data.pkl"

    if not os.path.exists(preprocessed_file):
        raise FileNotFoundError("Preprocessed data not found. Please run the base script first.")

    # Load preprocessed data
    preprocessor = DataPreprocessor.load_preprocessed_data(preprocessed_file)
    df = preprocessor.df

    # Define parameters for filtering and sampling
    min_comments = 5
    max_comments = 50
    num_users = 100

    # Filter and sample data
    filtered_df = filter_users_by_comment_count(df, min_comments, max_comments)
    sampled_df = sample_users(filtered_df, num_users)

    # Save the filtered and sampled data to JSON
    output_path = "spheres/filtered_sampled_articles_with_threads.json"
    save_filtered_json(sampled_df, output_path)

if __name__ == "__main__":
    main()