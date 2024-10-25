# Preprocessing

## Workflow Notes

## Preprocessing-Notes

- Anpassen von Datentypen
** asterrix entgfernt?
- anwneden der strikten markdown formatierung in vs code

## Building the Base JSON Structure

### Data Loading and Initialization

- The script `build_base_json.py` begins by loading configurations from `config.json`.
- It initializes a `DataPreprocessor` with the path to the raw CSV data file containing the comments and user information.

### Data Processing Steps

- **Converting Date Columns**  
  Date columns such as `'PostingCreatedAt'`, `'ArticlePublishingDate'`, and `'UserCreatedAt'` are converted to datetime format. This standardization facilitates date manipulations and time-based analyses, such as calculating the time difference between events.

- **Handling Missing Values**  
  Missing values in text fields like `'PostingHeadline'` and `'PostingComment'` are filled with default strings (e.g., `'No Headline'`, `'No Comment'`). This ensures consistency in the data and prevents errors during processing that may occur due to `NaN` values.

- **Converting ID Columns**  
  ID columns (e.g., `'ID_Posting'`, `'ID_Posting_Parent'`, `'ID_CommunityIdentity'`, `'ID_Article'`) are filled with zeros where missing and converted to integer type. This standardization is crucial for maintaining the integrity of identifiers and facilitating the construction of hierarchical relationships between comments.

- **Creating New Features**  
  Additional features are created to enrich the dataset:
  - `'CommentLength'`: The length of each comment text.
  - `'DaysSinceUserCreation'`: The number of days between user account creation and the comment posting date.
  - `'IsReply'`: A boolean indicating whether the comment is a reply to another comment.
  - `'PostingHour'`: The hour of the day when the comment was posted.
  - `'PostingDayOfWeek'`: The day of the week when the comment was posted.

### Saving Preprocessed Data

- The preprocessed DataFrame is saved as a pickle file (`.pkl`) for efficient loading in subsequent steps. Using pickle serialization allows for faster read/write operations compared to repeatedly processing the raw CSV file.

### Building Comment Threads

- A `CommentThreadManager` is initialized with the preprocessed data.
- The method `build_comment_thread()` recursively constructs a hierarchical structure of comments and their replies, organizing them under their respective articles.
- Each comment includes detailed metadata, such as user information and timestamps, facilitating comprehensive analysis.

### Saving the Data Structure

- The comprehensive data structure, containing article information and comment threads, is saved to a JSON file. JSON format is chosen for its ability to represent nested structures and its compatibility with various data processing tools.

### Potential Reader Questions and Explanations

- **Why are missing values filled with default strings like `'No Headline'`?**  
  Filling missing text fields with default strings ensures all records have consistent formats, which is important for string operations and downstream text processing. It also provides a clear indication that the original value was missing.

- **Why are IDs converted to integers?**  
  Converting IDs to integers standardizes identifier formats and ensures proper functioning of hierarchical relationships and comparisons. Integer IDs are also more memory-efficient and faster to process.

- **Why save the data as a pickle file?**  
  Pickle files serialize Python objects, allowing for quick storage and retrieval of preprocessed data. This speeds up workflow by avoiding repeated preprocessing of raw data.

- **Why is the data structure saved in JSON format?**  
  JSON is ideal for representing the nested, hierarchical nature of comment threads. It's a widely supported format that's easy to read and parse, facilitating data exchange between different systems.

- **[Erklärung hier einfügen]**

## Generating Context Markdown Files

### Overview

- The script `build_context_md.py` processes the JSON data structure to generate Markdown files containing the comments and interactions of individual users.
- Each Markdown file represents a user's activity across various articles, formatted to retain the hierarchical structure of discussions.

### Key Functions

- **Token Counting**  
  The `count_tokens()` function encodes text using a specific tokenization model (e.g., `'cl100k_base'`) and counts the tokens. This is crucial for ensuring that the text length stays within the limits of language models used later in the pipeline.
  The Token count is also later used for filtering and sampling set creation.

- **User Activity Filtering**  
  Functions like `user_in_comment_or_replies()` and `filter_comments_by_user()` recursively search through comments and replies to extract only those relevant to a specific user. This isolates each user's contributions for targeted analysis.

- **User Activity Filtering**  
    We need to limit the context sphere by trying to put as much relevant data into it as possible, but without overflooding the sphere with data which is not relevant to the user.


- **Markdown Generation**  
  The `generate_comment_markdown()` function creates a Markdown-formatted representation of comments, including metadata and hierarchical indentation to reflect the structure of conversations.

### Processing All Users

- The script processes all users identified in the pickled DataFrame.
- For each user:
  - Extracts comments and relevant replies.
  - Generates a Markdown file containing their activity.
  - Stores user metadata (e.g., user ID, username, token count) in a separate JSON file for reference.

### Potential Reader Questions and Explanations

- **Why convert comments to Markdown format?**  
  Markdown provides a readable and structured text format that preserves the hierarchical nature of comments and replies. It is widely supported and easy to convert to other formats if needed. Using Markdown also makes it suitable for input into language models that process text data.

    ">" are used to display the intendation.
  The "markdownlint" extention in vs code was used to check on all markdown rules and validate the format.
  It was experimented with xml tags since anthropic is proposing this to indicate seperate blocks of context, many language models are also trained with xml formated data. The complex tree structure of comments and threads on the other and lead to many tokens used only to display the format. The intendation in markdown with the use of ">" turned out to be much more token efficient and easier to read for the human eye. Markdown is the current most common output langauge by language model and is also adviced to use as input format.

- **Why is token counting necessary?**  
  Token counts are important for managing inputs to language models, which often have maximum token limits. By counting tokens, we can ensure that the generated Markdown files are within acceptable size ranges for efficient processing.

- **Why focus on specific users?**  
  Isolating individual user activity allows for personalized analysis and reduces the complexity of the data processed in subsequent steps.

- **Why are some comment cutoff and some not?**
        - An assumption is, that if a user posts a comment in a thread, and this is the only comment in the thread, he read the parent post, since this is the post he replied to but he most probable did not read all answer to the own post. In the end it does not play any role, since the user does not post again. These comment can therefore be cutoff from the context sphere.
        - We cutoff all comments from other users, where the targeted user has no interaction with. Meaning he did not reply to it at any point later time. We could´ve used the indications of up and down votes to further look into the point in time where the user stopped interacting, but since this is a metric which hard grasp and hard to display in natural language, for the sake of simplicity this is not included. Display in natural language which users gave where a thumbs up or down is another challenge and shold rather be aggregated or looked into with another approach. It could be used to strength or weakend the final classification by verifing the beahviour of the user with up and down votes on other posts.

- **[Erklärung hier einfügen]**

## Validation of Data

### Purpose

- The script `validation_script.py` ensures data consistency between the preprocessed pickled DataFrame and the JSON data structure.
- It validates that each user's occurrence count matches across both datasets, confirming that no data was lost or duplicated during transformation.

### Validation Steps

- **Loading Data**  
  Both the pickled DataFrame and the JSON data structure are loaded into memory for analysis.

- **Counting User Occurrences**  
  - In the pickled DataFrame, the script counts how often each unique user name appears.
  - In the JSON data, it recursively searches through the comment threads to count occurrences of each user.

- **Comparing Counts**  
  The occurrence counts from both datasets are compared for each user. Any discrepancies are reported, indicating potential issues in the data transformation process.

### Potential Reader Questions and Explanations

- **Why is data validation necessary?**  
  Validating data ensures that the preprocessing steps preserved the integrity of the information. It helps identify and correct any errors introduced during data transformation, which is crucial for reliable analysis.

- **Why compare user occurrence counts?**  
  User occurrence counts are a straightforward metric to verify that all user comments have been accurately transferred between data formats.

- **[Erklärung hier einfügen]**

## Creating a Sample Set

### Objective

- The script `create_sample_set.py` generates a sample set of user Markdown files based on specified criteria, such as token count ranges (`MIN_TOKEN_COUNT`, `MAX_TOKEN_COUNT`) and sample size (`SAMPLE_SIZE`).
- This is helpful for testing, validation, or working with a manageable subset of data.

### Steps Taken

- **Loading Configuration**  
  Parameters including directory paths, token count limits, and sample size are loaded from `config.json`.

- **Sample Directory Creation**  
  A timestamped directory is created to store the sampled files, ensuring that samples are organized and do not overwrite previous ones.

- **Filtering Files**  
  - Metadata files containing token counts are read.
  - Files are filtered to include only those where the token count falls within the specified range.
  - Up to `SAMPLE_SIZE` files are selected to form the sample set.

- **Copying Files**  
  The selected Markdown files are copied into the sample directory for easy access and further processing.

### Potential Reader Questions and Explanations

- **Why is a sample set needed?**  
  Working with a sample set allows for quicker iterations during development and testing. It is also useful when computational resources are limited or when the full dataset is too large to process efficiently.

- **Why filter based on token count?**  
  Ensuring that samples fall within specific token count ranges is important for consistency and for meeting the input requirements of language models, which may have limitations on input size.

- **[Erklärung hier einfügen]**

## Configuration Parameters

- The `config.json` file contains various configuration parameters used throughout the preprocessing scripts. Externalizing configurations promotes flexibility and ease of modification without changing the code.

### Key Parameters

- **File Paths**
  - `"input_pkl_path"`: Path to the preprocessed pickled data.
  - `"input_json_path"`: Path to the JSON file containing comment threads.
  - `"input_csv_path"`: Path to the raw CSV data file.
  - `"output_folder_markdown_generation"`: Directory where generated Markdown files are saved.
  - `"output_folder_samples"`: Directory where sample sets are saved.

- **Token Count Limits**
  - `"MIN_TOKEN_COUNT"`: Minimum acceptable token count for samples.
  - `"MAX_TOKEN_COUNT"`: Maximum acceptable token count for samples.

- **Sample Size**
  - `"SAMPLE_SIZE"`: The number of files to include in the sample set.

### Potential Reader Questions and Explanations

- **Why are configurations externalized to a JSON file?**  
  External configuration files enhance maintainability and adaptability. They allow for easy updates to parameters without the need to modify the script code, reducing the risk of introducing errors.

- **[Erklärung hier einfügen]**

## Example Output

- An example Markdown output is provided in `example_output.md`.
- The file showcases a user's activity, including comments on various articles, formatted with headings and metadata.

### Structure

- **User Details**  
  At the top, user details such as username, user ID, gender, and account creation date are listed.

- **Article Sections**  
  Each article the user has commented on is presented with:
  - Article title and metadata (ID, publication date, channel, ressort, total comments).
  - A section for the user's comments, preserving the thread hierarchy.

- **Comments**  
  Comments include:
  - Headline (if available).
  - The text of the comment.
  - Timestamp of when the comment was created.

### Potential Reader Questions and Explanations

- **Why is the output structured this way?**  
  The structured format preserves important contextual information and the conversational flow, which is essential for comprehensive analysis by both humans and language models.

- **How does this format benefit further processing?**  
  By maintaining a consistent and detailed format, downstream processes like emotion analysis can more effectively parse and interpret the data.

- **[Erklärung hier einfügen]**

# LLM-Pipeline

## Emotion Analysis Data Models

### Overview

- The script `data_model.py` defines data models using Pydantic to structure the outputs of the emotion analysis performed by the language model.
- These models are based on Lisa Feldman Barrett's theory of constructed emotions, aiming for a nuanced understanding of emotional states.

### Key Models

- **`CoreAffectAnalysis`**  
  Represents the core affect dimensions:
  - **Valence**: Degree of pleasantness or unpleasantness.
  - **Arousal**: Level of activation or energy.

- **`EmotionalAspectExtended`**  
  Provides an in-depth analysis incorporating:
  - **Thought Process**: Detailed reasoning behind the analysis.
  - **Context**: Situational factors influencing emotion.
  - **Cognitive Appraisal**: User's interpretations and judgments.
  - **Conceptualization**: How language and cultural background shape emotion.
  - **Cultural Influence**: Societal norms and values affecting emotional experience.
  - **Predictions and Simulations**: Influence of past experiences and expectations.
  - **Emotional Dynamics**: Changes in emotion over time or in response to interactions.
  - **Nuanced Classification**: A refined categorization of the emotional aspect.

- **`EmotionAnalysisOutput`**  
  Combines the analyses into a single structured output for easy processing.

### Potential Reader Questions and Explanations

- **Why use Pydantic models?**  
  Pydantic provides type validation and serialization of data structures, ensuring that the outputs conform to expected formats. This is crucial when parsing and validating responses from language models.

- **Why focus on Lisa Feldman Barrett's theory?**  
  Her theory emphasizes the constructed nature of emotions, providing a framework for a more dynamic and contextually grounded analysis, which is valuable for nuanced emotion detection.

- **Why are some models commented out (e.g., `EmotionalBlendAnalysis`, `UserNeedAnalysis`)?**  
  **[Erklärung hier einfügen]**

- **[Erklärung hier einfügen]**

## Saving Output to CSV

### Functionality

- The script `save_output_to_csv.py` provides a function to append the emotion analysis results to a CSV file.
- This includes model parameters and metadata for comprehensive record-keeping.

### Key Aspects

- **Appending Data**  
  Ensures that data is appended correctly, creating the file with headers if it doesn't exist.

- **Data Captured**  
  - Timestamp, run ID, user ID, batch ID, model name, and prompt template version.
  - Detailed fields from the `EmotionAnalysisOutput`, including thoughts and classifications.
  - Model parameters such as temperature and `top_p`.

### Potential Reader Questions and Explanations

- **Why save outputs to CSV?**  
  CSV files are widely used and compatible with many data analysis tools, making it easy to perform statistical analysis or visualization of the results.

- **[Erklärung hier einfügen]**

## Main Processing Script

### Overview

- The `main.py` script orchestrates the emotion analysis workflow, integrating the models, prompt templates, and the language model to process the user comments.

### Key Steps

- **Loading Environment and Configurations**  
  Utilizes environment variables and dynamically imports necessary modules and configurations.

- **Creating the Emotion Analysis Chain**  
  Combines the prompt templates with the language model and the Pydantic output parser to form a processing pipeline.

- **Processing Input Files in Batches**  
  - Reads Markdown files containing user comments.
  - Processes them in batches to improve efficiency and manage resources.
  - Uses a unique batch ID for tracking and logging.

- **Handling Outputs and Feedback**  
  - Optionally sends feedback to a client (e.g., Langsmith) for logging or further analysis.
  - Saves the outputs to a CSV file for record-keeping and analysis.

### Potential Reader Questions and Explanations

- **Why process files in batches?**  
  Batching enhances performance by reducing overhead and allows for parallel processing, which is beneficial when working with large datasets.

- **What is the role of prompt templates?**  
  Prompt templates guide the language model to produce outputs that align with the expected data structures and analysis requirements, ensuring consistency.

- **Why are model parameters like `temperature` and `top_p` important?**  
  These parameters influence the randomness and creativity of the language model's output, affecting how deterministic or varied the responses are.

- **What does the UUID batch ID represent?**  
  It uniquely identifies each batch run, facilitating tracking, and debugging, especially when integrating with logging systems.

- **Why use the `collect_runs()` context manager?**  
  It captures the runs for potential inspection, debugging, or logging, allowing for better traceability of the processing pipeline.

- **[Erklärung hier einfügen]**

## Conclusion

This document outlines the workflow of the master's thesis project, detailing the preprocessing steps and the language model pipeline. It highlights the key components of each script, explains the reasoning behind various decisions, and anticipates questions that a reader unfamiliar with the code might have.

[Erklärung hier einfügen] (Additional explanations and domain-specific knowledge to be added later.)
