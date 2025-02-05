from icecream import ic
from pathlib import Path
from tqdm import tqdm
import json
from src_llm_pipeline.emotion_classification import request_emotion_analysis_with_user_id
import csv
import os


# --- load variables from config.json ---
with open("src_llm_pipeline/config.json", "r") as config_file:
    config = json.load(config_file)


sample_folder = config["sample_folder"]


# Function to write a single successful result to CSV.
def write_results_to_csv(user_id, msg_history_step1, msg_history_step2, output_csv="output_results.csv"):
    # Expected header and order of fields:
    header = [
        "user_id",
        "role_setting_prompt_1", "role_feedback_prompt_1", "step_1_result",
        "role_setting_prompt_2", "role_feedback_prompt_2", "step_2_result"
    ]
    
    # Create row by extracting the first three expected fields from each message history.
    # If any field is missing, use an empty string.
    def get_field(messages, index):
        try:
            return messages[index].get("content", "")
        except IndexError:
            return ""
    
    row = [
        user_id,
        get_field(msg_history_step1, 0),  # role_setting_prompt_1
        get_field(msg_history_step1, 1),  # role_feedback_prompt_1
        get_field(msg_history_step1, 2),  # step_1_result
        get_field(msg_history_step2, 0),  # role_setting_prompt_2
        get_field(msg_history_step2, 1),  # role_feedback_prompt_2
        get_field(msg_history_step2, 2),  # step_2_result
    ]
    
    # Check if file exists so we know whether to write the header.
    file_exists = os.path.isfile(output_csv)
    
    # Open the file in append mode.
    with open(output_csv, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="|")
        # If file didn't exist (or is empty) write the header.
        if not file_exists or os.stat(output_csv).st_size == 0:
            writer.writerow(header)
        writer.writerow(row)
    print("Wrote result for user_id:", user_id)


# Main processing function
def process_markdown_files_in_folder():
    results = []  # (optional) store info if needed later
    folder_path = Path(f"src_llm_pipeline/inputs/{sample_folder}")
    print("--- Start of User Processing ---")
    for markdown_file in tqdm(folder_path.glob("*.md"), desc="Processing files"):
        file_stem = markdown_file.stem
        # Extract user id from the filename. Adjust splitting as needed.
        try:
            user_id_from_filename = file_stem.split("_")[1]
        except IndexError:
            print("Filename format incorrect for:", file_stem)
            continue

        print("START ANALYSIS OF USER:", user_id_from_filename)
        context_sphere = markdown_file.read_text().strip()
    
        try:
            # These two calls return lists of dictionaries (the “message histories”).
            message_history_step1, message_history_step2 = request_emotion_analysis_with_user_id(
                context_sphere=context_sphere,
                user_id=user_id_from_filename,
            )
            print("Processed item:", file_stem)
            # Immediately write the successful result to the CSV.
            write_results_to_csv(user_id_from_filename, message_history_step1, message_history_step2)
        except Exception as e:
            print(f"Skipping item {file_stem} due to:", e)
            continue  # Skip to the next file
        
        # Optionally, store the result tuple if needed for other purposes.
        results.append((user_id_from_filename, message_history_step1, message_history_step2))
    
    print("--- End of User Processing ---")
    return results

# Example usage:
if __name__ == "__main__": # adjust the folder name as needed
    results = process_markdown_files_in_folder()