import pymysql
from pymysql.err import *

from lib.config.config_file import Config
from lib.custom_exception import DBConnectionError, DBQueryError, DBException


class MySqlDBManager:

    def __init__(self, database_name):
        """
        method to create the database connection
        :param database_name: communication
        """

        config = Config.get_config()
        database_details = config.get(database_name)
        connection_details = config.get(database_details['CONNECTION'])

        self.db_conn = pymysql.connect(
            host=connection_details['HOST'],
            user=connection_details['USERNAME'],
            password=connection_details['PASSWORD'],
            database=database_details['DATABASE']
        )

    def rollback(self):
        """
            Rollback the changes
        """
        if self.db_conn:
            self.db_conn.rollback()
    def save(self):
        """
        :Note: It commits all transaction
        """
        # commit the database transaction
        self.db_conn.commit()

    def end(self):
        """close the db connection"""
        self.db_conn.close()

    def get_cursor(self):
        """method to return the db cursor"""

        return self.db_conn.cursor(pymysql.cursors.DictCursor)

    def run_query(self, query, arguments=None, fetch=False, count=0, primary_key=False):
        """
        method to run the query in the db_connection and based on the fetch status will share the response
        :param query: query
        :param arguments: [12,12]
        :param fetch: true or false
        :param count: Natural Number if specific count required
        :param primary_key: True/False
        :return:
        """

        try:
            cursor = self.get_cursor()

            if arguments:
                cursor.execute(query, arguments)
            else:
                cursor.execute(query)

            output = None

            if fetch:
                result = cursor.fetchall()

                if count == 1 and len(result) >= count:
                    output = result[0]
                elif 1 < count <= len(result):
                    output = result[0:count]
                else:
                    output = result
            else:
                if primary_key:
                    cursor.execute("SELECT LAST_INSERT_ID() as id")
                    result = cursor.fetchone()
                    output = result['id']
                else:
                    output = cursor.rowcount

            return output

        except (DataError, IntegrityError, NotSupportedError, ProgrammingError) as ex:
            raise DBConnectionError('DB Connection creation Error::%s' % ex)
        except (DatabaseError, InterfaceError, InternalError, OperationalError) as ex:
            raise DBConnectionError('DB Connection creation Error::%s' % ex)
        except ValueError as ex:
            raise DBQueryError('Exception while executing the Query::%s' % ex)
        except Exception as ex:
            raise DBConnectionError('Un-handled exception in mysql manager::%s' % ex)