import json
from langsmith import Client
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path

def load_config():
    current_script_dir = Path(__file__).resolve().parent
    config_path = current_script_dir.parent / 'config.json'
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config

def add_runs_to_dataset():
    load_dotenv()

    config = load_config()

    client = Client()

    dataset_tag = config["dataset_tag"]
    delete_dataset = config["delete_dataset"]

    if dataset_tag == "default_dataset":
        dataset_name = "default_dataset_iterative_development_runs_last_14_days"
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d:%H:%M:%S")
        dataset_name = f"{dataset_tag}_{timestamp}"

    # Filter runs to add to the dataset
    runs = client.list_runs(
        project_name="LLM-Classification-Pipeline",
        run_type="chain",
        is_root=True,
        filter=f'has(tags, "{dataset_tag}")',
        error=False,
    )

    if not runs:
        print("No runs found matching the criteria.")
        return None

    if delete_dataset:
        if client.has_dataset(dataset_name=dataset_name):
            client.delete_dataset(dataset_name=dataset_name)
            print("Deleted existing dataset")
        dataset = client.create_dataset(
            dataset_name=dataset_name,
            description="Default Dataset for Langsmith Development runs last 14 days",
            inputs_schema={
                "type": "object",
                "title": "dataset_input_schema",
                "required": ["step_1_classification"],
                "properties": {
                    "step_1_classification": {
                        "type": "object"
                    }
                }
            },
            outputs_schema={
                "type": "object",
                "title": "dataset_output_schema",
                "required": ["step_2_classification_summary"],
                "properties": {
                    "step_2_classification_summary": {
                        "type": "string"
                    }
                }
            }
        )
        existing_run_ids = set()
    else:
        if client.has_dataset(dataset_name=dataset_name):
            dataset = client.read_dataset(dataset_name=dataset_name)
            print("Loaded existing dataset")
            # Fetch existing examples to avoid duplicates
            existing_examples = client.list_examples(dataset_id=dataset.id)
            existing_run_ids = {example.source_run_id for example in existing_examples if example.source_run_id}
        else:
            dataset = client.create_dataset(
                dataset_name=dataset_name,
                description="Default Dataset for Langsmith Development runs last 14 days",
                inputs_schema={
                    "type": "object",
                    "title": "dataset_input_schema",
                    "required": ["step_1_classification"],
                    "properties": {
                        "step_1_classification": {
                            "type": "object"
                        }
                    }
                },
                outputs_schema={
                    "type": "object",
                    "title": "dataset_output_schema",
                    "required": ["step_2_classification_summary"],
                    "properties": {
                        "step_2_classification_summary": {
                            "type": "string"
                        }
                    }
                }
            )
            print("Created new dataset")
            existing_run_ids = set()

    # Filter out runs that have already been added
    new_runs = [run for run in runs if run.id not in existing_run_ids]

    if not new_runs:
        print("All runs are already in the dataset.")
        return dataset.share_link if dataset.share_link else None

    # Add new runs to the dataset
    for run in new_runs:
        input_data = run.outputs.get("model-Step 1: Classification")
        output_data = run.outputs.get("model-Step 2: Summarization")

        if isinstance(input_data, str):
            input_data = json.loads(input_data)

        client.create_example(
            inputs={"step_1_classification": input_data},
            outputs={"step_2_classification_summary": output_data},
            metadata={"user_id": run.tags[1]},
            created_at=run.end_time,
            dataset_id=dataset.id,
            split="dev",
            source_run_id=run.id,
        )

    # Share the dataset to get a public link
    share_info = client.share_dataset(dataset_id=dataset.id)
    print(f"Your dataset is now public. Shareable link: {share_info["url"]}")

    return share_info

if __name__ == '__main__':
    link = add_runs_to_dataset()
    if link:
        print(f"Dataset link: {link}")