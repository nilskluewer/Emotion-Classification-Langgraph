import a_build_user_json_v7
import b_build_user_context
from helper_functions import get_all_user_ids


path_article_full_tree = 'spheres/JSON/articles_with_threads_full_tree.json'
user_id = 49126



a_build_user_json_v7.main(path_article_full_tree, user_id)



input_path = f'spheres/JSON/user_{user_id}_threads.json'
full_output_path = f'spheres/MD/user_{user_id}_threads_full.md'
modified_output_path = f'spheres/MD/user_{user_id}_threads_cleaned.md'
b_build_user_context.main(input_path, full_output_path, modified_output_path, user_id=user_id)