#https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-filters#unsafe_responses

FINISH_REASON_MAP = {
    0: "FINISH_REASON_UNSPECIFIED",
    1: "STOP",
    2: "MAX_TOKENS",
    3: "SAFETY",
    4: "RECITATION",
    5: "OTHER",
    6: "BLOCKLIST",
    7: "PROHIBITED_CONTENT",
    8: "SPII",
    9: "MALFORMED_FUNCTION_CALL",
}


#https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-filters#configurable-filters
CATEGORY_MAP = {
    0: "HARM_UNSPECIFIED",
    1: "HARM_HATE_SPEECH",
    2: "HARM_DANGEROUS_CONTENT",
    3: "HARM_HARASSMENT",
    4: "HARM_SEXUALLY_EXPLICIT",
    # Add other categories as necessary
}

PROBABILITY_MAP = {
    0: "PROBABILITY_UNSPECIFIED",
    1: "VERY_UNLIKELY",
    2: "UNLIKELY",
    3: "NEGLIGIBLE",
    4: "LIKELY",
    5: "VERY_LIKELY",
    # Add other probability levels if there are any
}

SEVERITY_MAP = {
    0: "SEVERITY_UNSPECIFIED",
    1: "HARM_SEVERITY_NEGLIGIBLE",
    2: "HARM_SEVERITY_MINOR",
    3: "HARM_SEVERITY_SERIOUS",
    4: "HARM_SEVERITY_EXTREME",
    # Add other severity levels if there are any
}

MESSAGE_MAP = {
    0: "Role-Setting-Prompt",
    1: "Role-Feedback-Prompt",
    2: "User_Task_Prompt",
    3: "Step 1: Classification",
    4: "user_task_",
    5: "Step 2: Summarization",
}