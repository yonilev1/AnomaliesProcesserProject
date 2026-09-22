import csv
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
                       CREATE TABLE IF NOT EXISTS Stations \
                       ( \
                           Id \
                           VARCHAR \
                       ( \
                           50 \
                       ) PRIMARY KEY,
                           Name VARCHAR \
                       ( \
                           100 \
                       ),
                           Sector VARCHAR \
                       ( \
                           100 \
                       ),
                           Status VARCHAR \
                       ( \
                           20 \
                       ),
                           CreatedAt DATETIME
                           ) \
                       """

        cursor.execute(create_table)
        conn.commit()
        logger.info("Table 'Stations' verified/created successfully.")

        csv_file_path = "/app/stations.csv"
        if os.path.exists(csv_file_path):
            with open(csv_file_path, 'r', encoding='utf-8') as f:
                csv_data = csv.reader(f)
                next(csv_data)  # דילוג על הכותרות

                insert_query = """
                               INSERT \
                               IGNORE INTO Stations (Id, Name, Sector, Status, CreatedAt)
                    VALUES ( \
                               %s, \
                               %s, \
                               %s, \
                               %s, \
                               CURRENT_TIMESTAMP \
                               ) \
                               """

                # לקיחת כל הרשומות מהקובץ כפי שהן
                records = list(csv_data)

                cursor.executemany(insert_query, records)
                conn.commit()
                logger.info(f"Loaded {cursor.rowcount} new records into 'Stations'.")
        else:
            logger.warning(f"File {csv_file_path} not found. Skipping data load.")

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