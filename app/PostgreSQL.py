import psycopg2

from qrlib.QRComponent import QRComponent
from qrlib.QREnv import QREnv

class PostgreSQL(QRComponent):
    def __init__(self):
        super().__init__()
        self.logger = self.run_item.logger
        self.conn = None
        self.cursor = None

        

    def load_vault(self):
        self.dbname = QREnv.VAULTS["postgresql"]["dbname"]
        self.user = QREnv.VAULTS["postgresql"]["user"]
        self.password = QREnv.VAULTS["postgresql"]["password"]
        self.host = QREnv.VAULTS["postgresql"]["host"]
        self.port = QREnv.VAULTS["postgresql"]["port"]

    def establish_connection(self):
        self.load_vault()
        
        try:
            # self.logger.info(f"Connecting to database server...")
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
        except Exception as e:
            self.logger.info(f"Failed to connect to database server")
            raise e

        try:
            self.logger.info(f"Getting database cursor...")
            self.cursor = self.conn.cursor()
        except Exception as e:
            self.logger.info(f"Failed to get database cursor")
            raise e
    
    

    def create_table(self):
        '''
        Creates the the required table into the database if not already there. If table exsists then skips the table creation.
        '''
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS movies (
            id SERIAL PRIMARY KEY,
            movie_name VARCHAR(255) NOT NULL,
            user_score INTEGER,
            storyline TEXT,
            genres VARCHAR(255),
            review_1 TEXT,
            review_2 TEXT,
            review_3 TEXT,
            review_4 TEXT,
            review_5 TEXT,
            status VARCHAR(50) NOT NULL
        );
        '''
        try:
            self.logger.info(f"Creating database table...")
            self.cursor.execute(create_table_query)
            self.conn.commit()
        except Exception as e:
            self.logger.info(f"Failed to create database table")
            raise e

    def insert_into_table(self, movie_name, user_score, storyline, genres, review_1, review_2, review_3, review_4, review_5, status):
        try:
            self.logger.info(f"Inserting into database table")
            self.cursor.execute("""
            INSERT INTO movies (movie_name, user_score, storyline, genres, review_1, review_2, review_3, review_4, review_5, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (movie_name, user_score, storyline, genres,
                 review_1, review_2, review_3, review_4, review_5, status)
            )
            self.conn.commit()
        except Exception as e:
            self.logger.info(f"Failed to insert into database table")
            self.conn.rollback()
            raise e
        
    def close_connection(self):
        try:
            self.logger.info(f"Closing database connection...")
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            self.logger.info(f"Failed to close database connection")
            raise e