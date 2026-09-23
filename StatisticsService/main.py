import pymongo
from pymongo import MongoClient
import logging
from dotenv import load_dotenv
import os
import  pandas as pd

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
        rew_data_collection = database["REW_COLLECTION"]
        statistics_collection = database["STATISTICS_COLLECTION"]

        df = pd.DataFrame(list(rew_data_collection.find()))

        stats = process_statistics(df)
        for element in stats:
            statistics_collection.updateOne(element['_id'], element)

        client.close()
    except Exception as e:
        raise Exception(
            "The following error occurred: ", e)


def process_statistics(df):
    stats = []
    summary = df.groupby('source_id').agg(
        total_count=('Value', 'count'),
        average_value=('Value', 'mean'),
        minimum_value=('Value', 'min'),
        maximum_value=('Value', 'max')
    ).reset_index()

    for row, index in summary.iterrows():
        stats.append({
            'source_id':row['SourceId'],
            'count':int(row['total_count']),
            'minimum_value':int(row['minimum_value']),
            'maximum_value': int(row['maximum_value'])
        })

    return stats
