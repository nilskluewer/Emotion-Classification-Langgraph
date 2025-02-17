"""
This script processes markdown files from a configured sample folder and conducts a emotion analysis on them.
Each file is handled individually (1:1) and moved immediately:
    • To the "successful" folder if processing succeeds.
    • To the "skipped" folder if an error occurs.
"""

from pathlib import Path
from tqdm import tqdm
import json
from src_llm_pipeline.emotion_analysis import request_emotion_analysis_with_user_id

# --- Load configuration variables from config.json ---
with open("src_llm_pipeline/config.json", "r") as config_file:
    config = json.load(config_file)

sample_folder = config["sample_folder"]

def process_markdown_files_in_folder():
    """
    Process all markdown files in the specified sample folder.
    For each file, attempt to process the file and move it to:
        - "successful" folder if processing succeeds.
        - "skipped" folder if an error occurs.
    """
    folder_path = Path("src_llm_pipeline/inputs") / sample_folder

    # Set up destination folders.
    successful_folder = folder_path / "successful"
    skipped_folder = folder_path / "skipped"
    successful_folder.mkdir(exist_ok=True)
    skipped_folder.mkdir(exist_ok=True)

    print("--- Start of User Processing ---")
    # Iterate over all markdown files in the sample folder.
    for markdown_file in tqdm(list(folder_path.glob("*.md")), desc="Processing files"):
        destination = None  # Destination folder for the file
        try:
            file_stem = markdown_file.stem
            tokens = file_stem.split("_")
            if len(tokens) < 2:
                raise ValueError(f"Filename format incorrect for: {file_stem}")
            user_id = tokens[1]

            print(f"\nSTART ANALYSIS OF USER: {user_id}")

            # Read the file content.
            context_sphere = markdown_file.read_text().strip()

            # Process the file and retrieve message histories.
            message_history_step1, message_history_step2 = request_emotion_analysis_with_user_id(
                context_sphere=context_sphere,
                user_id=user_id,
            )
            print(f"Processed file: {file_stem}")
            destination = successful_folder / markdown_file.name

        except Exception as e:
            print(f"Skipping file {markdown_file.name} due to error: {e}")
            destination = skipped_folder / markdown_file.name

        finally:
            try:
                # Move the file to the determined folder.
                markdown_file.rename(destination)
            except Exception as move_error:
                print(f"Failed to move file {markdown_file.name} to {destination}: {move_error}")

    print("--- End of User Processing ---")

if __name__ == "__main__":
    process_markdown_files_in_folder()