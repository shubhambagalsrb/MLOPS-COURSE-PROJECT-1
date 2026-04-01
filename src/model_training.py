import os
import pandas as pd
import joblib
from src.logger import get_logger
from src.custom_exception import CustomException
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from config.paths_config import *
from config.model_params import *
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from scipy.stats import randint 
from utils.common_functions import load_data, read_yaml
import mlflow

logger = get_logger(__name__)

class ModelTraining:

    def __init__(self,train_path, test_path, model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path
        self.target_variable = "booking_status"
        self.params_dist = LIGHTGBM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

        logger.info(f"Model Training initialized with train path: {self.train_path}, test path: {self.test_path}, model output path: {self.model_output_path}")

    def load_and_split_data(self):
        try:
            logger.info(f"Loading processed train and test data from: {self.train_path}, {self.test_path}")
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            X_train = train_df.drop(self.target_variable, axis=1)
            y_train = train_df[self.target_variable]
            X_test = test_df.drop(self.target_variable, axis=1)
            y_test = test_df[self.target_variable]

            logger.info("Data loaded and split into features and target successfully")
            return X_train, y_train, X_test, y_test
        except Exception as e:
            logger.error(f"Error occurred while loading and splitting data: {str(e)}")
            raise CustomException(f"Failed to load and split data", e)
    
    def train_lgbm(self, X_train, y_train):
        try:
            logger.info("Starting hyperparameter tuning using RandomizedSearchCV")
            lgb_estimator = lgb.LGBMClassifier(random_state=42)

            logger.info(f"Performing RandomizedSearchCV with parameters distribution: {self.params_dist} and random search parameters: {self.random_search_params}")
            random_search = RandomizedSearchCV(estimator=lgb_estimator, 
                                               param_distributions=self.params_dist, 
                                               n_iter=self.random_search_params["n_iter"], 
                                               cv=self.random_search_params["cv"], 
                                               random_state=42, 
                                               n_jobs=self.random_search_params["n_jobs"],
                                               verbose=self.random_search_params["verbose"],
                                               scoring=self.random_search_params["scoring"])
            
            logger.info("Fitting RandomizedSearchCV to training data")

            random_search.fit(X_train, y_train)
            logger.info(f"RandomizedSearchCV completed successfully with best parameters: {random_search.best_params_}")

            best_params = random_search.best_params_
            best_model = random_search.best_estimator_

            return random_search
        except Exception as e:
            logger.error(f"Error occurred during hyperparameter tuning: {str(e)}")
            raise CustomException(f"Failed to perform hyperparameter tuning", e)
    
    def evaluate_model(self, model, X_test, y_test):
        try:
            logger.info("Evaluating model on test data")
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred)
            rec = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            logger.info(f"Model evaluation metrics - Accuracy: {acc}, Precision: {prec}, Recall: {rec}, F1 Score: {f1}")
            return {
                "accuracy": acc,
                "precision": prec,
                "recall": rec,
                "f1_score": f1
            }
        except Exception as e:
            logger.error(f"Error occurred during model evaluation: {str(e)}")
            raise CustomException(f"Failed to evaluate model", e)
    
    def save_model(self, model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)
            joblib.dump(model, self.model_output_path)
            logger.info(f"Model saved successfully to: {self.model_output_path}")
        except Exception as e:
            logger.error(f"Error occurred while saving model to path: {self.model_output_path} : {str(e)}")
            raise CustomException(f"Failed to save model to path: {self.model_output_path}", e)
    
    def run(self):
        try:
            with mlflow.start_run(run_name="Model Training"):
                logger.info("Starting model training process")
                logger.info("Starting our MLFLOW Experiment for model training")

                logger.info("Logging the traininf and testing dataset to MLFLOW")

                mlflow.log_artifact(self.train_path, artifact_path="datasets")
                mlflow.log_artifact(self.test_path, artifact_path="datasets")

                X_train, y_train, X_test, y_test = self.load_and_split_data()
                random_search = self.train_lgbm(X_train, y_train)
                best_model = random_search.best_estimator_
                evaluation_metrics = self.evaluate_model(best_model, X_test, y_test)
                logger.info(f"Evaluation metrics for the best model: {evaluation_metrics}")

                self.save_model(best_model)

                logger.info("Logging the best model to MLFLOW")
                mlflow.log_artifact(self.model_output_path, artifact_path="models")
                
                logger.info("Logging the best model parameters and evaluation metrics to MLFLOW")
                
                mlflow.log_params(best_model.get_params())
                mlflow.log_metrics(evaluation_metrics)


                logger.info("Model training process completed successfully")

                return best_model, X_test, y_test
            
        except CustomException as ce:
            logger.error(f"Error occurred during model training process: {str(ce)}")
        
        finally:
            logger.info("Model training process ended")
    
if __name__ == "__main__":
    config = read_yaml(CONFIG_PATH)
    model_trainer = ModelTraining(train_path=PROCESSED_TRAIN_DATA_PATH, test_path=PROCESSED_TEST_DATA_PATH, model_output_path=MODEL_OUPUT_PATH)
    best_model, X_test, y_test = model_trainer.run()
    y_pred = best_model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    logger.info(f"Model evaluation metrics - Accuracy: {acc}, Precision: {prec}, Recall: {rec}, F1 Score: {f1}")

