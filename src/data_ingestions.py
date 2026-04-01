import os
import pandas as pd
from google.cloud import storage

from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException

from config.paths_config import *

logger = get_logger(__name__)

class DataIngestion:

    def __init__(self, config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.bucket_file_name = self.config["bucket_file_name"]
        self.train_test_ratio = self.config["train_ratio"]

        os.makedirs(RAW_DATA_DIR, exist_ok=True)
        logger.info(f"Data Ingestion initialized with bucket: {self.bucket_name}, file: {self.bucket_file_name}, train-test ratio: {self.train_test_ratio}")

    def download_csv_from_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.bucket_file_name)

            blob.download_to_filename(RAW_FILE_PATH)
            logger.info(f"File downloaded successfully to: {RAW_FILE_PATH}")

        except Exception as e:
            logger.error(f"Error occurred while downloading file from GCP: {str(e)}")
            raise CustomException(f"Failed to download file from GCP", e)

    def split_data_into_train_test(self):

        try:
            logger.info(f"Reading raw data from: {RAW_FILE_PATH}")
            df = pd.read_csv(RAW_FILE_PATH)

            train_df, test_df = train_test_split(df, test_size=1-self.train_test_ratio, random_state=42)

            train_df.to_csv(TRAIN_FILE_PATH, index=False)
            test_df.to_csv(TEST_FILE_PATH, index=False)
            logger.info(f"Train and test data saved successfully to: {TRAIN_FILE_PATH}, {TEST_FILE_PATH}")
        except Exception as e:
            logger.error(f"Error occurred while splitting data: {str(e)}")
            raise CustomException(f"Failed to split data", e)
    
    def run(self):

        try:
            logger.info("Starting data ingestion process")
            self.download_csv_from_gcp()
            self.split_data_into_train_test()
            logger.info("Data ingestion process completed successfully")
        
        except CustomException as ce:
            logger.error(f"Error occurred during data ingestion process: {str(ce)}")
        
        finally:
            logger.info("Data ingestion process ended")


if __name__ == "__main__":
    from utils.common_functions import read_yaml_file

    config = read_yaml_file(CONFIG_PATH)
    data_ingestion = DataIngestion(config)
    data_ingestion.run()
        