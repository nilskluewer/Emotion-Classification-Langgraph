import json
import os
import pickle
import glob
from tqdm import tqdm
import pandas as pd

# Load configuration
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

markdown_folder = config['output_folder_markdown_generation']
pkl_path = config['pkl_path_input_build_context']
json_path = config['input_json_path']

def load_data():
    with open(pkl_path, 'rb') as file:
        pkl_data = pickle.load(file)

    with open(json_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    return pkl_data, json_data

def validate_user_names():
    pkl_data, json_data = load_data()
    
    if 'UserCommunityName' not in pkl_data.columns:
        raise KeyError("Das Feld 'UserCommunityName' fehlt im DataFrame.")
    
    # Count occurrences in the PKL file (DataFrame)
    pkl_user_counts = pkl_data['UserCommunityName'].value_counts().to_dict()
    print(f"PKL User counts: {pkl_user_counts}")
    
    # Count occurrences in the JSON
    json_user_counts = {}
    for article_key, article_data in json_data.items():
        for thread in article_data.get('comment_threads', []):
            user_name = thread['user_name']
            json_user_counts[user_name] = json_user_counts.get(user_name, 0) + 1

    print(f"JSON User counts: {json_user_counts}")
    
    # Check Markdown files
    md_user_counts = {}
    md_files = glob.glob(os.path.join(markdown_folder, "user_*_comments_*_tokens.md"))
    for md_file in md_files:
        user_name = None
        # Extract the user_name from the markdown file
        with open(md_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("# Benutzeraktivität von "):
                    user_name = line[len("# Benutzeraktivität von "):].strip()
                    break

        if user_name:
            md_user_counts[user_name] = md_user_counts.get(user_name, 0) + 1  # Include markdown occurrence

    print(f"Markdown User counts: {md_user_counts}")

    # Validate and summarize
    user_names = set(pkl_user_counts.keys()) | set(json_user_counts.keys()) | set(md_user_counts.keys())
    
    successful_validations = 0
    failed_validations = 0
    
    for user_name in user_names:
        pkl_count = pkl_user_counts.get(user_name, 0)
        json_count = json_user_counts.get(user_name, 0)
        md_count = md_user_counts.get(user_name, 0) + 1  # +1 for the manual entry during creation in Markdown

        if pkl_count == json_count == md_count:
            successful_validations += 1
        else:
            failed_validations += 1
            print(f"Discrepancy for User Name {user_name}: PKL={pkl_count}, JSON={json_count}, MD={md_count}")

    print("\nValidation Summary:")
    print(f"Successful validations: {successful_validations}")
    print(f"Failed validations: {failed_validations}")

# Call the validation function
validate_user_names()