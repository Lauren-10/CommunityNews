from scn_src.db_connectors import MySQLConnector
import click

@click.command()
@click.argument('--user', help = 'your MySQL username')
@click.option('--password', help = 'your MySQL password', )
@click.argument('--permission', help = 'reader, writer, or admin')
@click.argument('--host' help = 'host of MySQL server')
@click.argument('--database', help = 'name of the database')

# def instantiate(user, password, permission, host, database): #do tou need 'self'?
#     db_user = MySQLConnector(user = user, password = password, permission = permission, host = host, database = database)
#     return db_user

db_admin = MySQLConnector('wthomps3', permission = 'admin')

if __name__ == "__main__":
    instantiate()