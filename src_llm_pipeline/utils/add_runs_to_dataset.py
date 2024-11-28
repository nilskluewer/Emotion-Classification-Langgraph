import json
from langsmith import Client
from dotenv import load_dotenv

def add_runs_to_dataset(delete_dataset):
    """
    Processes runs from the Langsmith client and creates or updates a dataset based on specified criteria.

    This function loads configuration data, checks for existing datasets, processes runs based on filters, 
    and adds examples to the dataset. If specified, it can also delete an existing dataset beforehand.

    :param delete_dataset: A boolean flag indicating whether to delete the existing dataset before proceeding.
    :return: Link to the dataset if available.
    :rtype: str
    """
    load_dotenv()

    # Load configurations
    with open('../config.json', 'r') as config_file:
        config = json.load(config_file)

    client = Client()
    dataset_name = "default_dataset_iterative_development_runs_last_14_days"

    # Filter runs to add to the dataset
    runs = client.list_runs(
        project_name="LLM-Classification-Pipeline",
        run_type="chain",
        is_root=True,
        filter='has(tags, "default_dataset")',
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
    else:
        if client.has_dataset(dataset_name=dataset_name):
            dataset = client.read_dataset(dataset_name=dataset_name)
            print("Loaded existing dataset")
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

    for run in runs:
        input_data = run.outputs.get("model-Step 1: Classification")
        output_data = run.outputs.get("model-Step 2: Summarization")

        if isinstance(input_data, str):
            input_data = json.loads(input_data)

        result = client.create_example(
            inputs={"step_1_classification": input_data},
            outputs={"step_2_classification_summary": output_data},
            metadata={"user_id": run.tags[1]},
            created_at=run.end_time,
            dataset_id=dataset.id,
            split="dev",
            source_run_id=run.id,
        )
        
    # Return the link to the dataset if applicable
    return result

if __name__ == '__main__':
    # Example usage
    link = add_runs_to_dataset(delete_dataset=True)