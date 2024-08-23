import build_user_json_v7
import build_user_context
from helper_functions import get_all_user_ids
from tqdm import tqdm
import concurrent.futures
import json
import os

PROGRESS_FILE = 'progress.json'

def load_progress():
    """
    Load the progress from the JSON file.

    Returns:
        set: A set of processed user IDs.
    """
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as file:
            return set(json.load(file))
    return set()

def save_progress(processed_user_ids):
    """
    Save the progress to the JSON file.

    Args:
        processed_user_ids (set): A set of processed user IDs.
    """
    with open(PROGRESS_FILE, 'w') as file:
        json.dump(list(processed_user_ids), file)

def process_user_data(user_id, path_article_full_tree):
    """
    Process data for a single user by generating JSON and Markdown files.

    Args:
        user_id (int): The ID of the user to process.
        path_article_full_tree (str): Path to the full tree JSON file.
    """
    # Generate user JSON
    build_user_json_v7.main(path_article_full_tree, user_id)

    # Define paths for input and output files
    input_path = f'spheres/JSON/user_{user_id}_threads.json'
    full_output_path = f'spheres/MD/user_{user_id}_threads_full.md'
    modified_output_path = f'spheres/MD/user_{user_id}_threads_cleaned.md'

    # Generate user context Markdown files
    build_user_context.main(input_path, full_output_path, modified_output_path)

def main():
    """
    Main function to process data for all users and display a progress bar.
    """
    # Path to the full tree JSON file
    path_article_full_tree = 'spheres/JSON/articles_with_threads_full_tree.json'

    # Get all user IDs
    user_ids = get_all_user_ids("../data/preprocessed/preprocessed_data.pkl")

    # Load processed user IDs
    processed_user_ids = load_progress()

    # Filter out already processed user IDs
    user_ids_to_process = [user_id for user_id in user_ids if user_id not in processed_user_ids]

    # Use ThreadPoolExecutor to process data for each user in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Create a list of futures
        futures = {executor.submit(process_user_data, user_id, path_article_full_tree): user_id for user_id in user_ids_to_process}

        # Use tqdm to display a progress bar
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Processing users"):
            try:
                # Wait for the future to complete
                future.result()
                # Mark user as processed
                processed_user_ids.add(futures[future])
                # Save progress
                save_progress(processed_user_ids)
            except Exception as e:
                user_id = futures[future]
                print(f"Error processing user {user_id}: {e}")

if __name__ == "__main__":
    main()