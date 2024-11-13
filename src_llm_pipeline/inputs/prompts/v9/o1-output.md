Certainly! It seems you'd like to restructure your code to achieve better tracing with LangSmith, allowing you to:

- **Visualize each step of your pipeline** in LangSmith with proper nesting of runs.
- **Create feedback for both LLM calls individually**.
- **Attach overall feedback to the entire run**, including only the most relevant feedback tags.

To accomplish this, we'll focus on:

1. **Restructuring your functions** to properly utilize the `@traceable` decorator and the `run_tree` parameter.
2. **Ensuring that each LLM call is logged as a child run** within the main run.
3. **Attaching feedback** individually to the LLM runs and the overall run.

I'll guide you through the necessary changes step by step, explaining how to modify your code to support better tracing in LangSmith.

---

### **Understanding LangSmith Tracing**

LangSmith uses a hierarchical structure called a **run tree** to represent the tracing of your application. Each run can have **child runs**, allowing you to visualize nested operations, such as individual function calls or LLM invocations, within a parent run.

By properly utilizing the `@traceable` decorator and managing the `run_tree`, you can:

- **Capture each function call** as a separate run.
- **Nest runs appropriately** to reflect the structure of your application.
- **Attach feedback** to individual runs or the overall run.

---

### **Restructuring Your Code for Better Tracing**

#### **1. Modify the Main Function to Accept a `run_tree` Parameter**

In your `request_emotion_analysis` function, you can accept a `run_tree` parameter. This allows you to manage child runs explicitly. Here's how you can modify the function signature:

```python
@traceable(
    run_type="chain",
    name="EmotionAnalysis Request",
    tags=[f"{model_name}"]
)
def request_emotion_analysis(
        user_id: int,
        response_schema: dict,
        response_schema2: dict,
        prompt: List[Content],
        role_play_prompt_without_context_for_eval: List[Content],
        context_sphere_for_eval: str,
        run_tree: RunTree,  # Accept run_tree as a parameter
        model_name: str = "gemini-1.5-flash-002",
        temperature: float = 1,
        top_p: float = 0.95,
) -> dict:
    ...
```

#### **2. Pass the `run_tree` Parameter to Nested Functions**

For each nested function where you want to create a child run, you should accept the `run_tree` parameter and create a child run within it.

##### **a) Modify the `call_api` Function**

Since `call_api` is where the LLM calls happen, we want to capture each LLM call as a separate child run.

```python
@traceable(name="llm", run_type="llm")
def call_api(prompt, generation_config, safety_settings, run_tree: RunTree) -> GenerationResponse:
    # Create a child run within the parent run_tree
    with run_tree.child(name="LLM Call", run_type="llm", inputs={'prompt': prompt}) as child_run:
        response = model.generate_content(
            contents=prompt,
            generation_config=generation_config,
            safety_settings=safety_settings,
            stream=False
        )
        # Attach outputs to the child run
        child_run.end(outputs={'response': response.text})
    return response
```

**Note:** The `@traceable` decorator automatically manages the run tree, so we can also rely on it to handle child runs. However, since we need to attach feedback to individual LLM runs, it's better to manage the child runs explicitly using `run_tree.child`.

##### **b) Modify Other Nested Functions**

If you have other functions where you want to capture runs, you can similarly accept the `run_tree` parameter and manage child runs.

For example:

```python
@traceable(name="Parse LLM Response Structure", run_type="parser")
def parse_model_response_to_data_model_structure(input_text, target_schema, run_tree: RunTree) -> dict:
    # Create a child run
    with run_tree.child(name="Parse Response", run_type="parser", inputs={'input_text': input_text}) as child_run:
        data = parse_emotion_analysis(text=input_text, schema=target_schema)
        child_run.end(outputs={'parsed_data': data})
    return data
```

#### **3. Pass the `run_tree` to LLM Calls and Nested Functions**

When calling these functions, pass the `run_tree` to ensure the child runs are correctly nested.

```python
# In request_emotion_analysis
response = call_api(
    prompt=prompt,
    generation_config=generation_config,
    safety_settings=default_safety_settings,
    run_tree=run_tree  # Pass the run_tree
)
```

Similarly, for the follow-up analysis:

```python
# In create_holistic_analysis
response_2 = call_api(
    prompt=prompt,
    generation_config=generation_config_2,
    safety_settings=default_safety_settings,
    run_tree=run_tree  # Pass the same run_tree to nest under the main run
)
```

#### **4. Attach Feedback to Individual LLM Runs**

To create feedback for both LLM runs individually, store the run ID of each LLM call. Since we're manually managing the child runs, we can capture their IDs.

Modify the `call_api` function to return the `response` and the `child_run`:

```python
def call_api(prompt, generation_config, safety_settings, run_tree: RunTree) -> Tuple[GenerationResponse, RunTree]:
    with run_tree.child(name="LLM Call", run_type="llm", inputs={'prompt': prompt}) as child_run:
        response = model.generate_content(
            contents=prompt,
            generation_config=generation_config,
            safety_settings=safety_settings,
            stream=False
        )
        child_run.end(outputs={'response': response.text})
    return response, child_run
```

Now, when you call `call_api`, you'll get `response` and `child_run`:

```python
response, llm_run = call_api(
    prompt=prompt,
    generation_config=generation_config,
    safety_settings=default_safety_settings,
    run_tree=run_tree
)
```

You can then attach feedback to `llm_run`:

```python
client.create_feedback(
    llm_run.id,
    key="some_feedback_key",
    value="Feedback value for this LLM run",
    comment="Your comment",
    feedback_source_type="model"
)
```

Repeat this process for the second LLM call.

#### **5. Attach Feedback to the Overall Run**

Since you have the main `run_tree`, you can attach feedback to it directly:

```python
client.create_feedback(
    run_tree.id,
    key="overall_feedback",
    value="Overall feedback for the entire run",
    comment="Your comment",
    feedback_source_type="user"
)
```

---

### **Putting It All Together**

Let's adjust your code step by step.

#### **a) Update `request_emotion_analysis` Function**

```python
@traceable(
    run_type="chain",
    name="EmotionAnalysis Request",
    tags=[f"{model_name}"]
)
def request_emotion_analysis(
        user_id: int,
        response_schema: dict,
        response_schema2: dict,
        prompt: List[Content],
        role_play_prompt_without_context_for_eval: List[Content],
        context_sphere_for_eval: str,
        run_tree: RunTree,  # Accept run_tree
        model_name: str = "gemini-1.5-flash-002",
        temperature: float = 1,
        top_p: float = 0.95,
) -> dict:
    # Initialize the model
    model = GenerativeModel(model_name)

    # Attach User ID to the Trace for Logging
    client.create_feedback(
        run_tree.id,
        key="user_id",
        value=str(user_id),
        comment="ID of the current processed user"
    )

    # Configure generation parameters
    generation_config = GenerationConfig(
        response_mime_type="application/json",
        response_schema=response_schema,
        temperature=temperature,
        top_p=top_p,
        max_output_tokens=8000,
    )

    # Call the first LLM API
    response, llm_run1 = call_api(
        prompt=prompt,
        generation_config=generation_config,
        safety_settings=default_safety_settings,
        run_tree=run_tree  # Pass run_tree to nest under the main run
    )

    # Attach feedback to the first LLM run
    send_feedback_to_trace(
        response=response,
        client=client,
        run_tree=llm_run1  # Use llm_run1 to attach feedback to this LLM run
    )

    # Process the response
    parsed_data = parse_model_response_to_data_model_structure(
        input_text=response.text,
        target_schema=response_schema,
        run_tree=run_tree  # Pass run_tree if you want to trace this function
    )

    # Validate response
    is_valid = validate_response_property_order(
        parsed_data,
        response_schema,
        run_tree=run_tree
    )

    # Attach validation feedback to the main run
    client.create_feedback(
        run_tree.id,
        key="llm_output_format_validation",
        score=is_valid,
        comment="1 = True: The model used the correct propertyOrder. False, the model did not!"
    )

    # Prepare for the second LLM call
    second_task_prompt = Content(role="user", parts=[Part.from_text(read_prompts("user_task_followup_prompt.md"))])
    prompt = append_message(prompt, second_task_prompt)

    # Call the second LLM API
    python_dict, content_from_response_2, llm_run2 = create_holistic_analysis(
        response=response,
        prompt=prompt,
        run_tree=run_tree
    )

    # Add the response to message history
    message_history = append_message(prompt, content_from_response_2)

    # Convert message history to dict
    dict_list = convert_to_dict(message_history)

    return dict_list
```

#### **b) Update `call_api` Function**

```python
def call_api(prompt, generation_config, safety_settings, run_tree: RunTree) -> Tuple[GenerationResponse, RunTree]:
    with run_tree.child(name="LLM Call", run_type="llm", inputs={'prompt': prompt}) as child_run:
        response = model.generate_content(
            contents=prompt,
            generation_config=generation_config,
            safety_settings=safety_settings,
            stream=False
        )
        child_run.end(outputs={'response': response.text})
    return response, child_run
```

#### **c) Update `create_holistic_analysis` Function**

```python
def create_holistic_analysis(response: GenerationResponse, prompt: List[Content], run_tree: RunTree) -> Tuple[Any, list[Content], RunTree]:
    try:
        generation_config_2 = GenerationConfig(
            temperature=temperature,
            top_p=top_p,
            max_output_tokens=8000,
        )

        # Call the second LLM API
        response_2, llm_run2 = call_api(
            prompt=prompt,
            generation_config=generation_config_2,
            safety_settings=default_safety_settings,
            run_tree=run_tree  # Pass run_tree
        )

        # Process the response
        python_dict = {"empty": "empty"}  # Update as needed

        content_from_response_2 = response_2.candidates[0].content

        # Return llm_run2 to allow attaching feedback
        return python_dict, content_from_response_2, llm_run2

    except IndexError:
        print("Error")
```

#### **d) Attach Feedback to the Second LLM Run**

In your main function after calling `create_holistic_analysis`, you can attach feedback to `llm_run2`:

```python
# After getting the response from create_holistic_analysis
python_dict, content_from_response_2, llm_run2 = create_holistic_analysis(
    response=response,
    prompt=prompt,
    run_tree=run_tree
)

# Attach feedback to the second LLM run
send_feedback_to_trace(
    response=response_2,
    client=client,
    run_tree=llm_run2  # Use llm_run2 to attach feedback
)
```

#### **e) Attach Overall Feedback to the Main Run**

After all processing is complete, you can attach any overall feedback to `run_tree.id`:

```python
client.create_feedback(
    run_tree.id,
    key="overall_feedback",
    value="Overall feedback for the entire run",
    comment="Your comment",
    feedback_source_type="user"
)
```

---

### **Final Adjusted Functions**

Please note that for brevity, only key functions are shown adjusted. You'll need to make similar adjustments to other nested functions if you wish to trace them individually.

---

### **Additional Notes**

- **Using the RunTree API:** By explicitly creating child runs using `with run_tree.child(...)`, you have full control over how runs are nested and can attach feedback to each run individually.

- **Passing `run_tree` Parameter:** Ensure that any function where you want to create child runs accepts the `run_tree` parameter.

- **Consistent Run IDs:** By managing runs explicitly, you can capture run IDs for feedback and logging purposes.

- **Feedback Attachment:** You can attach feedback to any run by using its `id`. This allows you to differentiate feedback for each LLM call and the overall process.

---

### **Example of Updated Code Snippets**

Here's an example of how your `call_api` function would look after adjustments:

```python
def call_api(prompt, generation_config, safety_settings, run_tree: RunTree) -> Tuple[GenerationResponse, RunTree]:
    model = GenerativeModel(model_name)
    with run_tree.child(name="LLM Call", run_type="llm", inputs={'prompt': prompt}) as child_run:
        response = model.generate_content(
            contents=prompt,
            generation_config=generation_config,
            safety_settings=safety_settings,
            stream=False
        )
        # Attach outputs to the child run
        child_run.end(outputs={'response': response.text})
    return response, child_run
```

And your `request_emotion_analysis` function would be called like this:

```python
def process_markdown_files_in_folder(batch_id, dataset_name):
    results = []
    # ...
    for markdown_file in folder_path.glob("*.md"):
        # ...
        # Create a top-level run tree for each user
        with RunTree(name="Emotion Analysis Pipeline", run_type="chain", inputs={'user_id': user_id_from_filename}) as run_tree:
            result = request_emotion_analysis(
                user_id=user_id_from_filename,
                response_schema=schema_with_specific_ordering,
                response_schema2=schema_with_specific_ordering_holistic_profile,
                prompt=role_play_prompt,
                role_play_prompt_without_context_for_eval=role_play_prompt_without_context,
                context_sphere_for_eval=context_sphere,
                run_tree=run_tree  # Pass the run_tree
            )
        results.append(result)
    return results
```

---

### **Conclusion**

By restructuring your functions to accept the `run_tree` parameter and manually creating child runs, you can:

- **Visualize each step** of your pipeline in LangSmith with proper nesting.
- **Attach feedback to individual LLM runs**, allowing for granular analysis.
- **Attach overall feedback** to the main run for high-level insights.

This approach provides better tracing and makes it easier to debug and monitor your application.

---

### **Next Steps**

- **Test the Adjusted Code:** Run your application with the adjusted code to ensure that the tracing works as expected.

- **Verify in LangSmith:** Check the LangSmith dashboard to see if the runs are nested correctly and feedback is attached appropriately.

- **Further Adjustments:** If needed, further adjust other functions to capture more detailed tracing.

- **Feedback Tags:** Ensure that feedback tags are meaningful and consistent to facilitate easy filtering and analysis in LangSmith.

---

If you have any questions or need further clarification on any part of the code adjustments, feel free to ask!