import logging
import os
from dotenv import load_dotenv
import mysql.connector

logging.basicConfig(
        filename='/app/logs/project_logs.log',
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
logger = logging.getLogger()

def main():
    logger.info("Starting the Station Loader script...")
    try:
        load_dotenv()
        host = os.getenv("DB_HOST", "mysql")
        user = os.getenv("DB_USER", "root")
        password = os.getenv("DB_PASSWORD", "root")
        database = os.getenv("DB_NAME", "anomalies_db")

        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor()

        create_table = """
        CREATE TABLE IF NOT EXISTS Stations (
            Id VARCHAR(50) PRIMARY KEY,
            Name VARCHAR(100),
            Sector VARCHAR(100),
            Status VARCHAR(20),
            CreatedAt DATETIME
        )
        """

        cursor.execute(create_table)
        conn.commit()

        logger.info("Table 'Stations' verified/created successfully.")

    except mysql.connector.Error as err:
        logger.error(f"Database error occurred: {err}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()
            logger.info("Database connection closed.")

if __name__ == "__main__":
    main()