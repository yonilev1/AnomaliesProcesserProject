import pymongo
from narwhals import Datetime
from pymongo import MongoClient
import logging
from dotenv import load_dotenv
import os
import  pandas as pd
from datetime import datetime
import time

logging.basicConfig(
    filename='/app/logs/project_logs.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

def main():
    try:
        load_dotenv()
        uri = os.getenv("URI")
        client = MongoClient(uri)
        database = client[os.getenv("MONGO_DB_NAME")]
        rew_data_collection = database[os.getenv("REW_COLLECTION")]
        statistics_collection = database[os.getenv("STATISTICS_COLLECTION")]
        logger.info('connected do mongoDb')

        while True:
            time.sleep(int(os.getenv("TIME_TO_GET_STATS")))

            data = pd.DataFrame(list(rew_data_collection.find()))

            if len(data) == 0:
                logger.info("No raw data found in MongoDB yet.")
                continue

            start_time = datetime.now()
            stats, totals = process_statistics(data)
            for element in stats:
                (statistics_collection.update_one
                 (
                    {'_id': element['_id']},
                    {'$set': element},
                    upsert=True
                ))
            end_time = datetime.now()
            logger.info(f"""processed {totals['total_stations']} stations,
             with {totals['total_measurements']} measurements,
            it took {end_time- start_time}.
            """)

    except Exception as e:
        logger.error(f"Critical error in main loop: {e}")
        raise Exception(
            "The following error occurred: ", e)
    finally:
        client.close()



def process_statistics(df):
    stats = []
    summary = df.groupby('source_id').agg(
        total_count=('value', 'count'),
        average_value=('value', 'mean'),
        minimum_value=('value', 'min'),
        maximum_value=('value', 'max'),
        last_reading_at=('timestamp', 'max')
    ).reset_index()

    total_count = 0

    for index, row in summary.iterrows():
        total_count += int(row['total_count'])
        stats.append({
            '_id':row['source_id'],
            'measurements_count':int(row['total_count']),
            'average_value':float(row['average_value']),
            'min_value':float(row['minimum_value']),
            'max_value': float(row['maximum_value']),
            'last_reading_at': row['last_reading_at'],
            'computed_at': datetime.now()
        })

    totals = {
        'total_stations': len(stats),
        'total_measurements': total_count
    }
    return stats, totals

if __name__ == "__main__":
    main()
