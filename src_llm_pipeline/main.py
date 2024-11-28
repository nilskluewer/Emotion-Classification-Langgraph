import uuid
from utils.add_runs_to_dataset import add_runs_to_dataset

from llm_call import process_markdown_files_in_folder


if __name__ == '__main__':
    random_uuid = uuid.uuid4()
    
    # TODO set tags for the run
    result = process_markdown_files_in_folder()
    
    # TODO use tag for dataset creation
    # Add runs to dataset
    link = add_runs_to_dataset()

    
    #print(result)

