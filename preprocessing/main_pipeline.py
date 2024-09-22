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
CHUNK_SIZE = 22
TOKEN_LOWER_BOUND = 500  # Minimum number of tokens
TOKEN_UPPER_BOUND = 80000   # Maximum number of tokens
DESIRED_SAMPLE_SIZE = 500000
MAX_WORKERS = 22  # oder eine andere Zahl, die für Ihr System geeignet ist
FAILED_USERS_FILE = 'failed_users.json'

def load_failed_users():
    if os.path.exists(FAILED_USERS_FILE):
        with open(FAILED_USERS_FILE, 'r') as file:
            return set(json.load(file))
    return set()

def save_failed_users(failed_user_ids):
    with open(FAILED_USERS_FILE, 'w') as file:
        json.dump(list(failed_user_ids), file)

def create_output_directory():
    """Create a directory for the current sample run."""
    dir_name = f"{TIMESTAMP}_tokens_{TOKEN_LOWER_BOUND}_{TOKEN_UPPER_BOUND}_samples_{DESIRED_SAMPLE_SIZE}"
    full_path = os.path.join(OUTPUT_BASE_DIR, dir_name)
    os.makedirs(full_path, exist_ok=True)
    return full_path

def create_full_output_directory(base_dir):
    full_dir = os.path.join(base_dir, 'full')
    os.makedirs(full_dir, exist_ok=True)
    return full_dir

def create_cleaned_output_directory(base_dir):
    cleaned_dir = os.path.join(base_dir, 'cleaned')
    os.makedirs(cleaned_dir, exist_ok=True)
    return cleaned_dir

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

def count_tokens(text):
    """Count the number of tokens in the given text using tiktoken."""
    encoder = tiktoken.get_encoding("cl100k_base")  # Using the gpt2 model encoding as an example
    tokens = encoder.encode(text)
    return len(tokens)

def validate_output(input_path):
    """Check if the cleaned .md output meets token criteria and print details if rejected."""
    if os.path.exists(input_path):
        with open(input_path, 'r', encoding='utf-8') as file:
            content = file.read()
            token_count = count_tokens(content)
            if TOKEN_LOWER_BOUND <= token_count <= TOKEN_UPPER_BOUND:
                return True
            else:
                print(f"File {input_path} has {token_count} tokens and was rejected.")
    return False

def process_user_data(user_id, path_article_full_tree, full_output_dir, cleaned_output_dir):
    """Process data for a single user."""
    json_path = f'spheres/JSON/user_{user_id}_threads.json'

    a_build_user_json_v7.main(path_article_full_tree, user_id)

    full_output_path = os.path.join(full_output_dir, f'user_{user_id}_threads_full.md')
    cleaned_output_path = os.path.join(cleaned_output_dir, f'user_{user_id}_threads_cleaned.md')
    b_build_user_context.main(json_path, full_output_path, cleaned_output_path, user_id)

    # Check if the cleaned .md meets the token criteria
    if not validate_output(cleaned_output_path):
        # If criteria not met, delete both .md files and the JSON file
        os.remove(full_output_path)
        os.remove(cleaned_output_path)
        os.remove(json_path)
        return False

    # After processing, delete the JSON file
    os.remove(json_path)

    return True

def main():
    """Main function to process user data."""
    base_output_dir = create_output_directory()
    full_output_dir = create_full_output_directory(base_output_dir)
    cleaned_output_dir = create_cleaned_output_directory(base_output_dir)

    path_article_full_tree = 'spheres/articles_with_threads_full_tree.json'
    user_ids = get_all_user_ids("../data/preprocessed/preprocessed_data.pkl")
    processed_user_ids = load_progress()
    failed_user_ids = load_failed_users()
    user_ids_to_process = [user_id for user_id in user_ids if user_id not in processed_user_ids and user_id not in failed_user_ids]
    random.shuffle(user_ids_to_process)

    samples_saved = 0

    while samples_saved < DESIRED_SAMPLE_SIZE and user_ids_to_process:
        chunk = user_ids_to_process[:CHUNK_SIZE]
        user_ids_to_process = user_ids_to_process[CHUNK_SIZE:]

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(process_user_data, user_id, path_article_full_tree, full_output_dir, cleaned_output_dir): user_id for user_id in chunk}
            for future in concurrent.futures.as_completed(futures):
                user_id = futures[future]
                if future.result():
                    processed_user_ids.add(user_id)
                    samples_saved += 1
                    print(f"Sample saved: {samples_saved}/{DESIRED_SAMPLE_SIZE}")
                else:
                    failed_user_ids.add(user_id)
                if samples_saved >= DESIRED_SAMPLE_SIZE:
                    break

        save_progress(processed_user_ids)
        save_failed_users(failed_user_ids)

    clear_progress()
    # Optional: Möchten Sie auch die fehlgeschlagenen User zurücksetzen?
    os.remove(FAILED_USERS_FILE)

if __name__ == "__main__":
    main()