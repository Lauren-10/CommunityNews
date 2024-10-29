from scn_src.sql_pipeline import feeds_to_sql
from scn_src.db_connectors import MySQLConnector
import click

@click.command()
@click.option('--rss_feed_csv', type=click.Path(exists=True), help='The file path to your .csv containing feeds') 
@click.option('--feeds_table', type=str, help='The name of your MySQL table.')

def cli(rss_feed_csv, feeds_table):
    '''Command-line interface for the feeds_to_sql function. Sends finalized rss feed list to MySQL.'''

    #Initiates DBConnector
    db_admin = MySQLConnector('wthomps3', permission = 'admin')


    #Run command
    feeds_to_sql(
        db_admin=db_admin,
        rss_feed_csv=rss_feed_csv,
        table_name=feeds_table,
    )

if __name__ == "__main__":
    cli()
