"""NEEDS WORK: DBCONNECTOR CLASS"""
from scn_src.sql_pipeline import feeds_to_sql
from scn_src.db_connectors import MySQLConnector
import click

@click.command()
@click.argument('--rss_feed_csv', type=click.Path(exists=True), help='The file path to your .csv containing feeds') 
@click.argument('--table_name', help='The name of your MySQL table.')
#@click.argument('--connector_name', INFO TO CONSTITUTE MySQLConector)

def cli(rss_feed_csv, table_name, connector_name):
   
    #Initiates DBConnector
    db_connector = MySQLConnector(connector_name)

    #Run command
    feeds_to_sql(
        db_connector,
        rss_feed_csv=rss_feed_csv,
        table_name=table_name,
    )

if __name__ == "__main__":
    cli()