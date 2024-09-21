# NOTE: Das funktioniert nicht, da die struktur im sample npsäter nicht aussreicht um ealle beteiligten im thread abzubilden

# full_thread_sampling.py
from typing import Dict

import pandas as pd
import numpy as np
import json
import os
from build_base_json import DataPreprocessor, CommentThreadManager  # Assuming the base script is named base_script.py

def load_full_tree_json(full_tree_path: str) -> Dict:
    """
    Load the full comment threads from a JSON file if it exists.

    Args:
        full_tree_path (str): The path to the full tree JSON data.

    Returns:
        Dict: The loaded JSON data as a dictionary.
    """
    if os.path.exists(full_tree_path):
        print(f"Loading full tree JSON from {full_tree_path}")
        with open(full_tree_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return None

def save_full_tree_json(df: pd.DataFrame, full_tree_path: str):
    """
    Save the full comment threads to a JSON file.

    Args:
        df (pd.DataFrame): The preprocessed data.
        full_tree_path (str): The path where the full tree JSON data will be saved.
    """
    print("Creating full tree JSON...")
    thread_manager = CommentThreadManager(df)
    articles_with_threads = thread_manager.get_article_threads()

    with open(full_tree_path, 'w', encoding='utf-8') as f:
        json.dump(articles_with_threads, f, indent=2)
    print(f"Full tree JSON saved to {full_tree_path}")

def sample_users_from_full_tree(full_tree_data: Dict, num_users: int) -> Dict:
    """
    Sample a specified number of users from the full tree data.

    Args:
        full_tree_data (Dict): The full tree data loaded from JSON.
        num_users (int): Number of users to sample.

    Returns:
        Dict: A dictionary containing only the sampled users' threads.
    """
    # Extract all unique user IDs from the full tree data
    all_users = set()
    for article in full_tree_data.values():
        for thread in article['comment_threads']:
            all_users.add(thread['user_id'])
            for reply in thread['replies']:
                all_users.add(reply['user_id'])

    # Sample user IDs
    sampled_users = np.random.choice(list(all_users), size=min(num_users, len(all_users)), replace=False)

    # Filter threads to include only sampled users
    def filter_threads(threads):
        return [
            thread for thread in threads
            if thread['user_id'] in sampled_users or any(reply['user_id'] in sampled_users for reply in thread['replies'])
        ]

    sampled_data = {}
    for article_id, article in full_tree_data.items():
        sampled_data[article_id] = {
            **article,
            'comment_threads': filter_threads(article['comment_threads'])
        }

    return sampled_data

def save_sampled_json(sampled_data: Dict, output_path: str):
    """
    Save the sampled data to a JSON file.

    Args:
        sampled_data (Dict): The sampled data.
        output_path (str): The path where the JSON data will be saved.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sampled_data, f, indent=2)
    print(f"Sampled data saved to {output_path}")

def main():
    print("Checkmark 0")
    preprocessed_file = r"../../data/preprocessed/preprocessed_data.pkl"
    full_tree_path = "../spheres/articles_with_threads_full_tree.json"

    if not os.path.exists(preprocessed_file):
        raise FileNotFoundError("Preprocessed data not found. Please run the base script first.")
    print("Checkmark 1")
    # Load or create the full tree JSON
    full_tree_data = load_full_tree_json(full_tree_path)
    if full_tree_data is None:
        print("rebuild full JSON tree")
        # Load preprocessed data to create the full tree JSON
        preprocessor = DataPreprocessor.load_preprocessed_data(preprocessed_file)
        df = preprocessor.df
        save_full_tree_json(df, full_tree_path)
        full_tree_data = load_full_tree_json(full_tree_path)
    print("Checkmark 2")
    # Define parameters for sampling
    num_users = 1

    # Sample users from the full tree data
    sampled_data = sample_users_from_full_tree(full_tree_data, num_users)

    # Save the sampled data to JSON
    output_path = f"spheres/sampled_articles_with_threads_{num_users}.json"
    save_sampled_json(sampled_data, output_path)

if __name__ == "__main__":
    print("executemain")
    main()