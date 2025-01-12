from src_llm_pipeline.utils.add_runs_to_dataset import add_runs_to_dataset
from icecream import ic
from pathlib import Path
from tqdm import tqdm
import json
from src_llm_pipeline.emotion_classification import request_emotion_analysis_with_user_id

# --- load variables from config.json ---
with open("src_llm_pipeline/config.json", "r") as config_file:
    config = json.load(config_file)


sample_folder = config["sample_folder"]


# @traceable(name="Batch Processing Emotion Classifications", type="chain")
def process_markdown_files_in_folder():
    results = []  # To store the results for all processed files
    folder_path = Path(f"src_llm_pipeline/inputs/{sample_folder}")
    ic("--- Start of User Processing ---")
    # for markdown_file in folder_path.glob("*.md"):
    for markdown_file in tqdm(folder_path.glob("*.md"), desc="Processing files"):
        # Extract user ID from the markdown file name
        file_stem = markdown_file.stem
        user_id_from_filename = file_stem.split("_")[1]  # Assuming consistent naming
        ic("START ANALYSIS OF USER: ", user_id_from_filename)

        # Get context sphere for processing
        context_sphere = markdown_file.read_text().strip()
    
        try:
            result = request_emotion_analysis_with_user_id(
            context_sphere=context_sphere,
            user_id=user_id_from_filename,
        )
            # Process the result if no exception occurred
            print(f"Processed item: {file_stem}")
        except Exception as e:
            print(f"Skipping item {file_stem} due to: {e}")
            continue  # Skip to the next iteration
        

        results.append(result)
    ic("--- End of User Processing ---")
    return results  # Return after processing all files


if __name__ == "__main__":
    

    result = process_markdown_files_in_folder()

    # TODO use tag for dataset creation
    # Add runs to dataset
    # print("--- Wait 20sec to for runs POST to complete ---")
    # time.sleep(20)
    # link = add_runs_to_dataset()

    # print(result)
