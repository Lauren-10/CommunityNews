from scn_src.confidence_intervals import auto_precision_recall
from langchain_openai import ChatOpenAI
from scn_src.schema_instantiation import Article
from scn_src.prompt_draft import prompt
import click

@click.command()
@click.option('--bootstrap_iterations', type=int, help="Specifies the number of  precision, recall, and f1 scores calculated.")
@click.option('--llm_model', type=str, help="Specifies the model name for the LLM.")
@click.option('--llm_temperature', type=float, help="Temperature for the LLM (controls randomness).")
@click.option('--ground_truth_csv', type=click.Path(exists=True), help="Directory path to the ground truth CSV file.")

def cli(bootstrap_iterations, llm_model, llm_temperature, ground_truth_csv):
    
    #Initialize Prompt Template Object
    prompts = prompt()

    # Initialize the LLM object
    llm = ChatOpenAI(temperature=llm_temperature, model=llm_model)
    
    # Define the schema for the output, see if we want this to be adjustable
    schema = Article
    tags_to_extract = ['p','span','a','div']

    # Run the function
    auto_precision_recall(
        bootstrap_iterations=bootstrap_iterations,
        llm=llm,
        prompts=prompts,
        schema=schema,
        tags_to_extract=tags_to_extract,
        ground_truth_csv=ground_truth_csv
        )
    
if __name__ == "__main__":
    cli()