import json
# from difflib import get_close_matches
from mysql.connector import connect, Error
import config
import logging


class Dictionary:

    def __init__(self, db_engine):
        logging.info("Dictionary Started.")
        self.db_engine = db_engine
        if self.db_engine == 'mysql':
            # Database and Table creation
            try:
                with connect(
                    host = config.MYSQL_HOST,
                    user = config.MYSQL_USER,
                    password = config.MYSQL_PASSWORD
                ) as conn:
                    print(conn)
                    with conn.cursor(buffered=True) as cursor:
                        cursor.execute(f"show databases like '{config.MYSQL_DATABASE}'")
                        results = cursor.fetchall()
                        if results:
                            logging.info(f"Database {config.MYSQL_DATABASE} already exist.")
                        else:
                            logging.info(f"Creating database named {config.MYSQL_DATABASE}")
                            cursor.execute(f"create database {config.MYSQL_DATABASE}")
                            cursor.execute("show databases")
                            for db in cursor:
                                print(db)
                            logging.info(f"Database {config.MYSQL_DATABASE} created successfully.")
                        
                        conn.database = config.MYSQL_DATABASE
                        cursor.execute(f"show tables like '{config.MYSQL_TABLE}'")
                        results = cursor.fetchall()
                        if results:
                            logging.info(f"Table {config.MYSQL_TABLE} already exist.")
                            cursor.execute(f"select count(*) from {config.MYSQL_TABLE}")
                            row_cnt = cursor.fetchall()
                            if row_cnt[0][0] > 0:
                                logging.info(f"{row_cnt[0][0]} rows of data exist in table {config.MYSQL_TABLE}.")
                            else:
                                # Data Insertion in table
                                logging.info(f"Inserting data into table {config.MYSQL_TABLE}.")
                                data = json.load(open("data.json"))
                                data_list = [(key, value) for key, values in data.items() for value in values]
                                insert_list = "insert into Dictionary (Expression, Definition) values (%s, %s)"
                                cursor.executemany(insert_list, data_list)
                                cursor.execute("select * from Dictionary LIMIT 5")
                                for row in cursor:
                                    print(row)
                                logging.info(f"Data inserted successfully in table {config.MYSQL_TABLE}.")
                                conn.commit()

                        else:
                            logging.info(f"Creating table {config.MYSQL_TABLE} in {config.MYSQL_DATABASE}.")
                            cursor.execute(f"create table {config.MYSQL_TABLE} (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,\
                                Expression VARCHAR(100), Definition VARCHAR(10000))")
                            cursor.execute("show tables")
                            for table in cursor:
                                print(table)
                            logging.info(f"Table {config.MYSQL_TABLE} created successfully.")

                            # Data Insertion in table
                            logging.info(f"Inserting data into table {config.MYSQL_TABLE}.")
                            data = json.load(open("data.json"))
                            data_list = [(key, value) for key, values in data.items() for value in values]
                            insert_list = "insert into Dictionary (Expression, Definition) values (%s, %s)"
                            cursor.executemany(insert_list, data_list)
                            cursor.execute("select * from Dictionary LIMIT 5")
                            for row in cursor:
                                print(row)
                            logging.info(f"Data inserted successfully in table {config.MYSQL_TABLE}.")
                        conn.commit()
            except Error as e:
                logging.error(e)
    
    
    def db_query_mysql(self, word):
        if word == "\\end":
            logging.info("Closing Dictionary, Thank you!")
            return "Thank You!"
        else:
            try:
                con = connect(
                    host = config.MYSQL_HOST,
                    user = config.MYSQL_USER,
                    password = config.MYSQL_PASSWORD,
                    database = config.MYSQL_DATABASE
                )
                with con.cursor() as cursor:
                    logging.info(f"Searching for {word} in {config.MYSQL_TABLE} table.")
                    cursor.execute(f"select Definition from {config.MYSQL_TABLE} where Expression = '{word}'")
                    results = cursor.fetchall()

                if results:
                    logging.info(f"Found {word} in {config.MYSQL_TABLE} table.")
                    return results
                else:
                    logging.warning(f"{word} not found in {config.MYSQL_TABLE} table.")
                    return "The word you entered does not exist in the dictionary! Please try another word."
            except Error as e:
                logging.error(e)