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