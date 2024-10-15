from scn_src.confidence_intervals import auto_precision_recall
from langchain_openai import ChatOpenAI
from scn_src.schema_instantiation import Article
from scn_src.prompt_draft import prompt
import click

@click.command()
@click.argument('--num_chunks', default=20, type=click.INT, help="Specifies the number of times diagnostics are calculated.")
@click.argument('--llm-model', default="gpt-4", help="Specifies the model name for the LLM.")
@click.argument('--llm-temperature', default=0, type=click.FLOAT, help="Temperature for the LLM (controls randomness).") #is 0 a good default?
@click.argument('--tags-to-extract', multiple=True, help="HTML tags for the scraper to process.")
@click.argument('--ground-truth-df', type=click.Path(exists=True), help="Directory path to the ground truth CSV file.")

def cli(num_chunks, llm_model, llm_temperature, tags_to_extract, ground_truth_df):
    
    #Initialize Prompt Template Object
    prompts = prompt()

    # Initialize the LLM object
    llm = ChatOpenAI(temperature=llm_temperature, model=llm_model)
    
    # Define the schema for the output, see if we want this to be adjustable
    schema = Article
    
    # Run the function
    auto_precision_recall(
        num_chunks=num_chunks,
        llm=llm,
        prompts=prompts,
        schema=schema,
        tags_to_extract=list(tags_to_extract),
        ground_truth_df=ground_truth_df
        )
    
if __name__ == "__name__":
    cli()

'''
example in terminal:

python diagnostics_click.py --chunk-size 25 --llm-model "gpt-4" --llm-temperature 0.2 \
--tags-to-extract "<p>" "<h1>" --ground-truth-df "data/ground_truth.csv"
'''