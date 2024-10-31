from pathlib import Path
from dotenv import load_dotenv
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.utils.json_schema import dereference_refs
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from model import create_llm  # Assuming you have this utility function

# Import your new data model
from data_models import HolisticEmotionAnalysis

# Load environment variables
load_dotenv()

def load_system_prompt(filename: str, folder: Path) -> str:
    folder = Path(f"./prompts/{prompts_version}")
    return (folder / filename).read_text()

def load_input(filename: str, folder: Path) -> str:
    return (folder / filename).read_text()

def create_emotion_analysis_chain(model_temperature: float):
    # Get the schema for the new data model
    queries_schema = dereference_refs(HolisticEmotionAnalysis.model_json_schema())
    queries_schema.pop("$defs", None)

    # Create a simple prompt template
    prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(
                "You are an expert in emotion analysis using Lisa Feldman Barrett's theory of constructed emotion. "
                "Analyze the following context carefully."
            ),
            HumanMessagePromptTemplate.from_template("{context_sphere}")
        ]
    )

    # Create the LLM
    llm = create_llm(
        model_name=model_name,
        temperature=model_temperature,
        response_mime_type="application/json",
        response_schema=queries_schema,
    )

    # Create the parser for the new data model
    parser = PydanticOutputParser(pydantic_object=HolisticEmotionAnalysis)

    # Create the chain
    return prompt | llm | parser

def process_single_input(input_folder: Path, model_temperature: float) -> None:
    # Create the analysis chain
    emotion_analysis_chain = create_emotion_analysis_chain(model_temperature=model_temperature)
    
    # Get the first input file
    input_file = next(input_folder.glob("*.md"))
    
    # Load the context
    context_sphere = load_input(input_file.name, folder=input_folder)
    
    # Process the input
    result = emotion_analysis_chain.invoke(
        {"context_sphere": context_sphere}
    )
    
    # Print the result
    print(result)

if __name__ == "__main__":
    # Basic configuration
    input_folder = Path("./inputs/sp0")
    prompts_version = "v3"
    model_name = "gemini-1.5-pro-002"
    model_temperature = 0

    print("---- Starting Simple Analysis ----")
    process_single_input(
        input_folder=input_folder,
        model_temperature=model_temperature
    )