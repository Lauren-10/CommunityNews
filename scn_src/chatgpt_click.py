import click
from scn_src.sql_pipeline import chatgpt_to_sql
from scn_src.schema_instantiation import Article
from scn_src.lang_chain_utils import ChatOpenAI
from scn_src.db_connectors import MySQLConnector
from scn_src.prompt_draft import prompt

@click.command()
@click.option('--chunk_size', type=int, help="Specifies the number of URLs processed at a time.")
@click.option('--llm_model', type=str, help="Specifies the model name for the LLM.")
@click.option('--llm_temperature', type=float, help="Temperature for the LLM (controls randomness).")
@click.option('--final_table', type=str, help = 'name of MySQL table containing all articles')
@click.option('--multiprocessor_on', default=False, type = click.BOOL, help="Toggles multiprocessing capability.")

def cli(chunk_size, llm_model, llm_temperature, final_table, multiprocessor_on):
    """
    Command-line interface for the chatgpt_to_sql function. Selects a portion of the MySQL table that has not yet been
    processed by ChatGPT, separates rows into chunks of specified size, and runs scraper_inner_loop on each.
    """
    
    # Initialize the LLM object
    llm = ChatOpenAI(temperature=llm_temperature, model=llm_model)

    #Initialize the Schema object
    schema = Article

    #Initialize final prompt
    prompts = prompt()

    tags_to_extract = ['p','span','a','div']
    
    # Initialize the MySQLConnector object
    # db_admin = MySQLConnector(username=db_admin_username, permission=db_admin_permission)
    db_admin = MySQLConnector('wthomps3', permission = 'admin')
    
    # Run the main function
    chatgpt_to_sql(
        chunk_size=chunk_size,
        llm=llm,
        prompts=prompts,
        schema=schema,
        tags_to_extract=tags_to_extract,
        table_name=final_table,
        db_admin=db_admin,
        multiprocessor_on=multiprocessor_on
    )

if __name__ == "__main__":
    cli()
