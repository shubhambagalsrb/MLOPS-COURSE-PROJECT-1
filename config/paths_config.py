import os 


################# data ingestion #####

RAW_DATA_DIR = os.path.join("artifacts","raw_data")

RAW_FILE_PATH = os.path.join(RAW_DATA_DIR,"raw.csv")

TRAIN_FILE_PATH = os.path.join(RAW_DATA_DIR,"train.csv")
TEST_FILE_PATH = os.path.join(RAW_DATA_DIR,"test.csv")


CONFIG_PATH = "config/config.yaml"

################## Data Processing ##################

PROCESSED_DIR = 'artifacts/processed_data' 
PROCESSED_TRAIN_DATA_PATH = os.path.join(PROCESSED_DIR, 'processed_train.csv')
PROCESSED_TEST_DATA_PATH = os.path.join(PROCESSED_DIR, 'processed_test.csv')


####### Model Training ######

MODEL_OUPUT_PATH = os.path.join("artifacts", "Models", "lgbm_model.pkl")
