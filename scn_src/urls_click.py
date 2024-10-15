"""NEEDS WORK: 
DBCONNECTOR CLASS

parse_url needs to be rewritten to take SQL table name:
    tablename string to query string
    query string to df
    run parse as normal
"""

from scn_src.db_connectors import MySQLConnector
from scn_src.sql_pipeline import urls_to_sql
import click



@click.command()
@click.argument('--feeds_table', help='The name of your MySQL table.')
@click.argument('--final_table', help='The name of your MySQL table.')
#@click.argument('--connector_name', INFO TO CONSTITUTE MySQLConector)

def cli(feeds_table, final_table, connector_name):

    #Initiates MySQLConnector object
    db_connector = MySQLConnector(connector_name)

    #run command
    urls_to_sql(
        db_connector,
        feeds_table=feeds_table,
        final_table=final_table,
    )

if __name__ == "__main__":
    cli()


    