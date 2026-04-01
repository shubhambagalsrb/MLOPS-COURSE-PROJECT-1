
import os
import sys
import pandas as pd
from src.custom_exception import CustomException
from src.logger import get_logger
import yaml

logger = get_logger(__name__)


def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"YAML file not found at path: {file_path}")
        with open(file_path, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
        logger.info(f"YAML file read successfully from path: {file_path}")
        return config
    
    except Exception as e:
        logger.error(f"Error occurred while reading YAML file from path: {file_path}")
        raise CustomException(f"Failed to read YAML file from path: {file_path} : {str(e)}", sys)

def load_data(file_path):
    try:
        logger.info(f"Attempting to load data from path: {file_path}")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV file not found at path: {file_path}")
        df = pd.read_csv(file_path)
        logger.info(f"Data loaded successfully from path: {file_path}")
        return df
    
    except Exception as e:
        logger.error(f"Error occurred while loading data from path: {file_path}")
        raise CustomException(f"Failed to load data from path: {file_path} : {str(e)}", sys)