# full_thread_sampling.py

import pandas as pd
import numpy as np
import json
import os
from build_base_json import DataPreprocessor, CommentThreadManager  # Assuming the base script is named base_script.py

def save_full_tree_json(df: pd.DataFrame, full_tree_path: str):
    """
    Save the full comment threads to a JSON file if it doesn't already exist.

    Args:
        df (pd.DataFrame): The preprocessed data.
        full_tree_path (str): The path where the full tree JSON data will be saved.
    """
    if not os.path.exists(full_tree_path):
        print("Creating full tree JSON...")
        thread_manager = CommentThreadManager(df)
        articles_with_threads = thread_manager.get_article_threads()

        with open(full_tree_path, 'w', encoding='utf-8') as f:
            json.dump(articles_with_threads, f, indent=2)
        print(f"Full tree JSON saved to {full_tree_path}")
    else:
        print(f"Full tree JSON already exists at {full_tree_path}")

def sample_users_from_full_tree(df: pd.DataFrame, num_users: int) -> pd.DataFrame:
    """
    Sample a specified number of users from the full DataFrame.

    Args:
        df (pd.DataFrame): The preprocessed data.
        num_users (int): Number of users to sample.

    Returns:
        pd.DataFrame: DataFrame containing only the sampled users.
    """
    unique_users = df['ID_CommunityIdentity'].unique()
    sampled_users = np.random.choice(unique_users, size=min(num_users, len(unique_users)), replace=False)
    return df[df['ID_CommunityIdentity'].isin(sampled_users)]

def save_sampled_json(df: pd.DataFrame, output_path: str):
    """
    Save the sampled data to a JSON file.

    Args:
        df (pd.DataFrame): The sampled data.
        output_path (str): The path where the JSON data will be saved.
    """
    thread_manager = CommentThreadManager(df)
    articles_with_threads = thread_manager.get_article_threads()

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(articles_with_threads, f, indent=2)
    print(f"Sampled data saved to {output_path}")

def main():
    preprocessed_file = r"../data/preprocessed/preprocessed_data.pkl"
    full_tree_path = "spheres/full_tree_articles_with_threads.json"

    if not os.path.exists(preprocessed_file):
        raise FileNotFoundError("Preprocessed data not found. Please run the base script first.")

    # Load preprocessed data
    preprocessor = DataPreprocessor.load_preprocessed_data(preprocessed_file)
    df = preprocessor.df

    # Save the full tree JSON if not already done
    save_full_tree_json(df, full_tree_path)

    # Define parameters for sampling
    num_users = 100

    # Sample users from the full data
    sampled_df = sample_users_from_full_tree(df, num_users)

    # Save the sampled data to JSON
    output_path = f"spheres/sampled_articles_with_threads_num_users_{num_users}.json"
    save_sampled_json(sampled_df, output_path)

if __name__ == "__main__":
    main()