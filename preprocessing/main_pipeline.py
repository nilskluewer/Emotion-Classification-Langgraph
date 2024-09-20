import a_build_user_json_v7
import b_build_user_context
from helper_functions import get_all_user_ids
import concurrent.futures
import json
import os
import random
import tiktoken
import os
from datetime import datetime

# Am Anfang der Datei, fügen Sie diese Konstanten hinzu:
OUTPUT_BASE_DIR = 'samples'
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
PROGRESS_FILE = 'progress.json'
CHUNK_SIZE = 5
TOKEN_LOWER_BOUND = 10000   # Minimum number of tokens
TOKEN_UPPER_BOUND = 50000   # Maximum number of tokens
DESIRED_SAMPLE_SIZE = 50


def create_output_directory():
    """Create a directory for the current sample run."""
    dir_name = f"{TIMESTAMP}_tokens_{TOKEN_LOWER_BOUND}_{TOKEN_UPPER_BOUND}_samples_{DESIRED_SAMPLE_SIZE}"
    full_path = os.path.join(OUTPUT_BASE_DIR, dir_name)
    os.makedirs(full_path, exist_ok=True)
    return full_path


def load_progress():
    """Load the progress from a JSON file."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as file:
            return set(json.load(file))
    return set()

def clear_progress():
    """Clear the contents of the progress file."""
    with open(PROGRESS_FILE, 'w') as file:
        json.dump([], file)
    print(f"The progress has been cleared in {PROGRESS_FILE}.")

def save_progress(processed_user_ids):
    """Save the progress to a JSON file."""
    with open(PROGRESS_FILE, 'w') as file:
        json.dump(list(processed_user_ids), file)

def count_tokens(data):
    """Count the number of tokens in the given data using tiktoken."""
    encoder = tiktoken.get_encoding("gpt2")  # Using the gpt2 model encoding as an example
    text = json.dumps(data)  # Ensure the data is a JSON-formatted string
    tokens = encoder.encode(text)
    return len(tokens)

def validate_output(input_path):
    """Check if the JSON output meets token criteria and print details if rejected."""
    if os.path.exists(input_path):
        with open(input_path, 'r') as file:
            data = json.load(file)
            token_count = count_tokens(data)
            if TOKEN_LOWER_BOUND <= token_count <= TOKEN_UPPER_BOUND:
                return True
            else:
                print(f"File {input_path} has {token_count} tokens and was rejected.")
    return False


def process_user_data(user_id, path_article_full_tree, output_dir):
    """Process data for a single user."""
    a_build_user_json_v7.main(path_article_full_tree, user_id)
    input_path = f'spheres/JSON/user_{user_id}_threads.json'

    # Continue processing only if the JSON meets the token criteria
    if not validate_output(input_path):
        return False

    full_output_path = os.path.join(output_dir, f'user_{user_id}_threads_full.md')
    modified_output_path = os.path.join(output_dir, f'user_{user_id}_threads_cleaned.md')
    b_build_user_context.main(input_path, full_output_path, modified_output_path, user_id)
    return True

def main():
"""Main function to process user data."""
output_dir = create_output_directory()
path_article_full_tree = 'spheres/articles_with_threads_full_tree.json'
user_ids = get_all_user_ids("../data/preprocessed/preprocessed_data.pkl")
processed_user_ids = load_progress()
user_ids_to_process = [user_id for user_id in user_ids if user_id not in processed_user_ids]
random.shuffle(user_ids_to_process)

samples_saved = 0

while samples_saved < DESIRED_SAMPLE_SIZE and user_ids_to_process:
    chunk = user_ids_to_process[:CHUNK_SIZE]
    user_ids_to_process = user_ids_to_process[CHUNK_SIZE:]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_user_data, user_id, path_article_full_tree, output_dir): user_id for user_id in chunk}
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                processed_user_ids.add(futures[future])
                samples_saved += 1
                print(f"Sample saved: {samples_saved}/{DESIRED_SAMPLE_SIZE}")
                if samples_saved >= DESIRED_SAMPLE_SIZE:
                    break

    save_progress(processed_user_ids)

clear_progress()

if __name__ == "__main__":
    main()