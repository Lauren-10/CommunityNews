from scn_src.db_connectors import MySQLConnector
from scn_src.sql_pipeline import urls_to_sql
import click

@click.command()
@click.argument('feeds_table', type=str) #, help='The name of your MySQL table.')
@click.argument('final_table', type=str) #, help='The name of your MySQL table.')

def cli(feeds_table, final_table):
    '''Command-line interface for urls_to_sql function. Runs parse_url on all feeds in the datafram and updates specified 
    MySQL table with publication, is_uni_newspaper, url, article_title, and date columns filled. Author and is_student 
    fields will remain NULL.'''

    #Initiates MySQLConnector object
    db_admin = MySQLConnector('wthomps3', permission='admin')

    #Run command
    urls_to_sql(
        db_admin=db_admin,
        feeds_table=feeds_table,
        final_table=final_table,
    )

if __name__ == "__main__":
    cli()

'''WORKS!!!, Yet to succeed in calling with makefile'''
    