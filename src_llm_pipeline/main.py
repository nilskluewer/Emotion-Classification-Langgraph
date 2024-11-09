import uuid

from llm_call import process_markdown_files_in_folder


if __name__ == '__main__':
    random_uuid = uuid.uuid4()
    result = process_markdown_files_in_folder(batch_id=random_uuid, dataset_name = "Testing")
    print(result)

