from langsmith import Client
from langsmith import RunTree
from langsmith.run_helpers import traceable
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

client = Client()


@traceable(name="chain")
def chain_1(input, run_tree: RunTree) -> bool:
    print(input)
    return True, run_tree.id

@traceable(name="chain2",)
def chain_2(input, run_tree: RunTree) -> bool:
    print(input)
    return True, run_tree.id

@traceable(name="chain3")
def chain3(input, run_tree: RunTree) -> bool:
    print(input)
    return True, run_tree.id


result1, run_id = chain_1(input="1")
result2, run_id = chain_2(input="2")
