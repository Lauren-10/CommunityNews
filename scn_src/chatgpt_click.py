"""NEEDS WORK, review GPTcode"""

import click
from scn_src.sql_pipeline import chatgpt_to_sql
from scn_src.schema_instantiation import Article
from scn_src.lang_chain_utils import ChatOpenAI
from scn_src.db_connectors import MySQLConnector

@click.command()
@click.option('--chunk-size', default=20, type=int, help="Specifies the number of URLs processed at a time.")
@click.option('--llm-model', default="gpt-4", help="Specifies the model name for the LLM.")
@click.option('--llm-temperature', default=0.3, type=float, help="Temperature for the LLM (controls randomness).")
@click.option('--prompts', multiple=True, help="Prompts to pass to the LLM for processing.")
@click.option('--schema', default="Article", help="Specifies the structure of the LLM output.")
@click.option('--tags-to-extract', multiple=True, help="HTML tags for the scraper to process.")
@click.argument('table_name', type=str)
@click.option('--db-admin-username', prompt=True, help="MySQL client username.")
@click.option('--db-admin-permission', prompt=True, help="Permission level for the MySQL client.")
@click.option('--multiprocessor-on', is_flag=True, help="Toggles multiprocessing capability.")

def cli(chunk_size, llm_model, llm_temperature, prompts, schema, tags_to_extract, table_name, db_admin_username, db_admin_permission, multiprocessor_on):
    """
    Command-line interface for the chatgpt_to_sql function. Selects a portion of the MySQL table that has not yet been
    processed by ChatGPT, separates rows into chunks of specified size, and runs scraper_inner_loop on each.
    """
    
    # Initialize the LLM object
    llm = ChatOpenAI(temperature=llm_temperature, model=llm_model)
    
    # Initialize the MySQLConnector object
    db_admin = MySQLConnector(username=db_admin_username, permission=db_admin_permission)
    
    # Run the main function
    chatgpt_to_sql(
        chunk_size=chunk_size,
        llm=llm,
        prompts=list(prompts),
        schema=schema,
        tags_to_extract=list(tags_to_extract),
        table_name=table_name,
        db_admin=db_admin,
        multiprocessor_on=multiprocessor_on
    )

if __name__ == "__main__":
    cli()
