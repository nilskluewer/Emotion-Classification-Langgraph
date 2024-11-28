Certainly! Let's break down your request into key components and address each one systematically:

1. **Identify and list the important parts of the `Client` class for dataset management.**
2. **Explain how to create a shareable public dataset link.**
3. **Ensure proper handling of the dataset, including inserting only new runs that are not already present.**
4. **Demonstrate how to collect runs and add them to the dataset efficiently, making the best use of LangSmith.**

---

### 1. **Important Parts of the `Client` Class for Dataset Management**

The `Client` class provides several methods for managing datasets in LangSmith. Here are the key methods relevant to your use case:

- **Dataset Creation and Management:**
  - `create_dataset()`: Creates a new dataset.
  - `read_dataset()`: Retrieves a dataset by name or ID.
  - `has_dataset()`: Checks if a dataset exists.
  - `delete_dataset()`: Deletes a dataset.
  - `list_datasets()`: Lists datasets in your account.

- **Example (Data) Management within Datasets:**
  - `create_example()`: Adds a single example (data point) to a dataset.
  - `create_examples()`: Adds multiple examples to a dataset in bulk.
  - `list_examples()`: Lists examples within a dataset.
  - `update_example()`: Updates an existing example.
  - `update_examples()`: Updates multiple examples.
  - `delete_example()`: Deletes an example from a dataset.
  - `list_dataset_splits()`: Retrieves the splits (e.g., train, test) for a dataset.
  - `update_dataset_splits()`: Updates the splits for a dataset.

- **Dataset Sharing:**
  - `share_dataset()`: Creates a shareable link to your dataset, making it public.
  - `unshare_dataset()`: Revokes the shared link, making it private again.
  - `read_shared_dataset()`: Reads a shared dataset using its share token.
  - `list_shared_examples()`: Lists examples from a shared dataset.

---

### 2. **Creating a Shareable Public Dataset Link**

To make your dataset publicly accessible, you can use the `share_dataset()` method. This method creates a share token and returns a URL that others can use to view the dataset.

**Example Code:**

```python
dataset = client.read_dataset(dataset_name="your_dataset_name")
share_info = client.share_dataset(dataset_id=dataset.id)
print(f"Your dataset is now public. Shareable link: {share_info['url']}")
```

---

### 3. **Proper Handling of the Dataset: Inserting Only New Runs**

To ensure that you only add new runs (i.e., runs not already present in the dataset), you need to:

- Retrieve existing examples from the dataset.
- Collect the `source_run_id` from these examples.
- Compare the IDs of the runs you intend to add with the existing `source_run_id`s.
- Only add runs that are not already in the dataset.

**Implementation Steps:**

1. **Fetch Existing Examples:**

```python
existing_examples = client.list_examples(dataset_id=dataset.id)
existing_run_ids = {example.source_run_id for example in existing_examples if example.source_run_id}
```

2. **Filter Runs to Add Only New Ones:**

```python
new_runs = [run for run in runs if run.id not in existing_run_ids]
```

3. **Add New Runs to the Dataset:**

```python
for run in new_runs:
    # Process inputs and outputs
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
```

---

### 4. **Collecting Runs and Adding Them to the Dataset Efficiently**

Let's put it all together in your script, ensuring optimal use of LangSmith's capabilities.

**Updated Script:**

```python
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
    print(f"Your dataset is now public. Shareable link: {share_info.url}")

    return share_info.url

if __name__ == '__main__':
    link = add_runs_to_dataset()
    if link:
        print(f"Dataset link: {link}")
```

**Explanation:**

- **Managing Existing Runs:**
  - When loading the dataset, we fetch existing examples and collect their `source_run_id`s to avoid duplicates.
  - We define `existing_run_ids` to keep track of runs already in the dataset.
  
- **Adding Only New Runs:**
  - We filter the runs to include only those not present in `existing_run_ids`.
  - By checking `run.id not in existing_run_ids`, we ensure we don't add duplicates.

- **Sharing the Dataset:**
  - After adding new runs, we use `client.share_dataset()` to make the dataset public.
  - The shareable link is returned and printed.

---

### **Additional Tips for Making the Best Use of LangSmith:**

- **Batching Examples:**
  - If you have a large number of runs to add, consider using `client.create_examples()` to add them in bulk, which can improve performance.

- **Dataset Versioning:**
  - Leverage dataset versioning features to keep track of changes over time.
  - Use tags or timestamps when creating datasets to distinguish different versions.

- **Efficient Data Retrieval:**
  - When listing examples or runs, use appropriate filters and limits to minimize unnecessary data transfer.
  - Utilize pagination if dealing with large datasets.

- **Metadata Usage:**
  - Store useful metadata with your examples and runs, like `user_id`, `tags`, or other identifiers, to facilitate later analysis or filtering.

- **Error Handling:**
  - Implement proper error handling around API calls to gracefully handle network issues or API errors.

---

### **Final Note:**

By updating your script as shown and leveraging the `Client` methods effectively, you'll handle the dataset appropriately, avoid duplicate entries, and make your dataset publicly accessible with a shareable link.

Let me know if you have any questions or need further assistance!



Certainly! I'll apply my previous suggestions and integrate the additional information you provided. We'll modify the script to retrieve additional data from each `run`—such as `prompt_tokens`, `completion_tokens`, `total_tokens`, `run.tags`, `run.id`, and `run.feedback`—and include this information in the examples added to the dataset.

Here's the updated script:

```python
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
    """
    Processes runs from the Langsmith client and creates or updates a dataset based on specified criteria.
    This function retrieves runs, checks for duplicates, and adds new examples to the dataset.
    """
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
    runs = list(client.list_runs(
        project_name="LLM-Classification-Pipeline",
        run_type="chain",
        is_root=True,
        filter=f'has(tags, "{dataset_tag}")',
        error=False,
    ))

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
                "required": ["step_1_classification", "prompt_tokens", "completion_tokens", "total_tokens", "tags", "run_id", "feedback"],
                "properties": {
                    "step_1_classification": {"type": "object"},
                    "prompt_tokens": {"type": "integer"},
                    "completion_tokens": {"type": "integer"},
                    "total_tokens": {"type": "integer"},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "run_id": {"type": "string"},
                    "feedback": {"type": "object"},
                },
            },
            outputs_schema={
                "type": "object",
                "title": "dataset_output_schema",
                "required": ["step_2_classification_summary"],
                "properties": {
                    "step_2_classification_summary": {"type": "string"}
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
                    "required": ["step_1_classification", "prompt_tokens", "completion_tokens", "total_tokens", "tags", "run_id", "feedback"],
                    "properties": {
                        "step_1_classification": {"type": "object"},
                        "prompt_tokens": {"type": "integer"},
                        "completion_tokens": {"type": "integer"},
                        "total_tokens": {"type": "integer"},
                        "tags": {"type": "array", "items": {"type": "string"}},
                        "run_id": {"type": "string"},
                        "feedback": {"type": "object"},
                    },
                },
                outputs_schema={
                    "type": "object",
                    "title": "dataset_output_schema",
                    "required": ["step_2_classification_summary"],
                    "properties": {
                        "step_2_classification_summary": {"type": "string"}
                    }
                }
            )
            print("Created new dataset")
            existing_run_ids = set()

    # Filter out runs that have already been added
    new_runs = [run for run in runs if run.id not in existing_run_ids]

    if not new_runs:
        print("All runs are already in the dataset.")
        # Share the dataset to get a public link
        share_info = client.share_dataset(dataset_id=dataset.id)
        print(f"Your dataset is now public. Shareable link: {share_info.url}")
        return share_info.url

    # Add new runs to the dataset
    examples_to_add = []
    for run in new_runs:
        # Retrieve additional information from the run
        prompt_tokens = getattr(run, 'prompt_tokens', None)
        completion_tokens = getattr(run, 'completion_tokens', None)
        total_tokens = getattr(run, 'total_tokens', None)
        tags = getattr(run, 'tags', [])
        run_id = str(run.id)
        feedback = getattr(run, 'feedback_stats', {})

        # Handle the potential absence of specific tag indices
        tag_value = tags[2] if len(tags) > 2 else None

        input_data = run.outputs.get("model-Step 1: Classification")
        output_data = run.outputs.get("model-Step 2: Summarization")

        if isinstance(input_data, str):
            input_data = json.loads(input_data)

        # Prepare the inputs dictionary including additional data
        example_inputs = {
            "step_1_classification": input_data,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "tags": tags,
            "tag_value": tag_value,  # The specific tag if needed
            "run_id": run_id,
            "feedback": feedback,
        }

        example = {
            "inputs": example_inputs,
            "outputs": {"step_2_classification_summary": output_data},
            "metadata": {"user_id": tags[1]} if len(tags) > 1 else {},
            "created_at": run.end_time,
            "dataset_id": dataset.id,
            "split": "dev",
            "source_run_id": run.id,
        }
        examples_to_add.append(example)

    # Use bulk creation for efficiency
    client.create_examples(
        inputs=[ex["inputs"] for ex in examples_to_add],
        outputs=[ex["outputs"] for ex in examples_to_add],
        metadata=[ex["metadata"] for ex in examples_to_add],
        splits=[ex["split"] for ex in examples_to_add],
        source_run_ids=[ex["source_run_id"] for ex in examples_to_add],
        dataset_id=dataset.id,
    )

    # Share the dataset to get a public link
    share_info = client.share_dataset(dataset_id=dataset.id)
    print(f"Your dataset is now public. Shareable link: {share_info.url}")

    return share_info.url

if __name__ == '__main__':
    link = add_runs_to_dataset()
    if link:
        print(f"Dataset link: {link}")
```

### Explanation of Modifications:

- **Retrieving Additional Run Information:**
  - Used `getattr(run, 'attribute', default)` to safely retrieve `prompt_tokens`, `completion_tokens`, `total_tokens`, `tags`, `run.id`, and `run.feedback_stats`.
  - Handled cases where certain attributes might be absent by providing a default value (e.g., `None` or `{}`).

- **Updating the Inputs Schema:**
  - Expanded the `inputs_schema` to include the new fields: `prompt_tokens`, `completion_tokens`, `total_tokens`, `tags`, `run_id`, and `feedback`.
  - This ensures that the dataset schema matches the data we're adding.

- **Preparing the Inputs Dictionary:**
  - Created `example_inputs` to include all the required input data as well as the additional run information.
  - Included a safety check for `tags[2]`, as accessing an index that doesn't exist can raise an error. If `tags` doesn't have at least three elements, `tag_value` will be `None`.

- **Using Bulk Example Creation:**
  - Collected all examples into a list `examples_to_add`.
  - Used `client.create_examples()` to add all examples in a single API call, which is more efficient than adding them one by one.

- **Handling Metadata:**
  - Included `user_id` in the `metadata` if available from `tags`.

- **Sharing the Dataset:**
  - After adding new runs, used `client.share_dataset()` to make the dataset public and obtain a shareable link.

### Notes:

- **Error Handling:**
  - When accessing attributes like `run.prompt_tokens`, it's important to handle the possibility that they might be `None`.
  - The same applies to the `tags` list; we check its length before accessing an index.

- **Feedback Data:**
  - Included `run.feedback_stats` in the inputs under the key `feedback`.
  - Since feedback can sometimes be empty, we're defaulting to an empty dictionary `{}` if it's not present.

- **Source Run IDs:**
  - Ensured that we're using the `run.id` as the `source_run_id` when creating examples. This helps in avoiding duplicates in the future.

- **Efficiency:**
  - By collecting all examples and using `client.create_examples()` in bulk, we reduce the number of API calls and improve performance.

### Testing the Script:

- **Ensure Dependencies are Installed:**
  - Make sure you have the `langsmith` package installed.
  - Ensure that your `config.json` file contains the necessary configuration, such as `dataset_tag` and `delete_dataset`.

- **Running the Script:**
  - Execute the script. It will process the runs, add new examples to the dataset, and print out the shareable dataset link.

- **Validating the Dataset:**
  - Visit the shareable link to verify that the dataset includes the new examples with all the additional information.

### Making the Best Use of LangSmith:

- **Data Enrichment:**
  - By including detailed information from each `run`, the dataset becomes richer and more valuable for analysis.

- **Avoiding Duplicates:**
  - Tracking `source_run_id` and checking existing runs prevent duplicate entries, keeping the dataset clean.

- **Public Sharing:**
  - Using `share_dataset()` allows you to easily share your dataset with others or use it in public analyses.

Feel free to adjust the fields included in `inputs` or modify the schema as needed for your specific use case.

Let me know if you have any questions or need further assistance!