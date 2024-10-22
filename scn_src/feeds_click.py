from scn_src.sql_pipeline import feeds_to_sql
from scn_src.db_connectors import MySQLConnector
import click

@click.command()
@click.argument('rss_feed_csv', type=click.Path(exists=True)) #, help='The file path to your .csv containing feeds') 
@click.argument('table_name', type=str) #, help='The name of your MySQL table.')

def cli(rss_feed_csv, table_name):
    '''Command-line interface for the feeds_to_sql function. Sends finalized rss feed list to MySQL.'''

    #Initiates DBConnector
    db_admin = MySQLConnector('wthomps3', permission = 'admin')


    #Run command
    feeds_to_sql(
        db_admin=db_admin,
        rss_feed_csv=rss_feed_csv,
        table_name=table_name,
    )

if __name__ == "__main__":
    cli()

'''WORKS!!!, Yet to succeed in calling with makefile'''