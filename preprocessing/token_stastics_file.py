import json
import os

def load_config(config_path='config.json'):
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

def get_token_count_from_filename(filename):
    """
    Extract the token count from the filename assuming the format includes '_{token_count}_tokens'.
    """
    parts = filename.split('_')
    try:
        token_index = parts.index('tokens.md') - 1
        token_count = int(parts[token_index])
        return token_count
    except (ValueError, IndexError):
        return None

def adjust_for_tokenization_offset(token_count, offset=0.1):
    """
    Adjust the token count by a pre-defined offset percentage.
    This offset accounts for a simpler tokenizer's discrepancy with the final tokenizer in the pipeline.
    """
    adjusted_count = token_count * (1 - offset)
    return adjusted_count

def calculate_statistics(markdown_folder, offset=0.1):
    """
    Calculate the statistics using an adjusted token count for each file.
    """
    files = os.listdir(markdown_folder)
    adjusted_token_counts = []

    for filename in files:
        if filename.endswith('.md'):
            token_count = get_token_count_from_filename(filename)
            if token_count is not None:
                adjusted_token_count = adjust_for_tokenization_offset(token_count, offset)
                adjusted_token_counts.append(adjusted_token_count)

    total_files = len(adjusted_token_counts)
    total_adjusted_tokens = sum(adjusted_token_counts)
    avg_adjusted_tokens = total_adjusted_tokens / total_files if total_files > 0 else 0

    # Calculate average adjusted word count range per file
    avg_adjusted_word_count_range = (
        avg_adjusted_tokens * 60 // 100,
        avg_adjusted_tokens * 80 // 100
    )
    
    # Assuming 250 words per page, derive the estimated book pages for the average
    words_per_page = 250
    avg_adjusted_page_estimation_range = (
        avg_adjusted_word_count_range[0] // words_per_page,
        avg_adjusted_word_count_range[1] // words_per_page
    )

    return {
        "total_files": total_files,
        "total_adjusted_tokens": total_adjusted_tokens,
        "average_adjusted_tokens_per_file": avg_adjusted_tokens,
        "average_adjusted_word_count_range_per_file": avg_adjusted_word_count_range,
        "estimated_book_pages_range_per_file": avg_adjusted_page_estimation_range
    }

def save_statistics(statistics, markdown_folder):
    """
    Save the calculated statistics to a JSON file named '00_statistics_tokens.json'.
    """
    filepath = os.path.join(markdown_folder, '00_statistics_tokens.json')
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(statistics, f, indent=2)

def main():
    config = load_config()
    markdown_folder = config['output_folder_markdown_generation']

    # Offset value for subtraction is 10%, indicating our simpler tokenizer overestimates by 10%
    offset = 0.1
    print(f"Using a tokenization offset of {offset*100}% to account for discrepancies with the pipeline's tokenizer.")

    statistics = calculate_statistics(markdown_folder, offset)
    save_statistics(statistics, markdown_folder)

    print(f"\nStatistics calculated and saved:")
    print(f"Adjusted total token count: {statistics['total_adjusted_tokens']}")
    print(f"Average tokens per file (adjusted): {statistics['average_adjusted_tokens_per_file']}")
    print(f"Average word count range per file (adjusted): {statistics['average_adjusted_word_count_range_per_file']}")
    print(f"Estimated equivalent book pages range per file (considering 250 words per page): {statistics['estimated_book_pages_range_per_file']} pages")

if __name__ == "__main__":
    main()