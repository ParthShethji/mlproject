from statistics import LinearRegression
import sys
import os

from sklearn.ensemble import AdaBoostRegressor, GradientBoostingRegressor, RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from src.logger import logging
from src.exception import CustomException
import pandas as pd
import numpy as np
import catboost
from src.utils import evaluate_models, save_object
import xgboost
from dataclasses import dataclass
from sklearn.linear_model import LinearRegression

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts', 'model.pkl')
    
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Splitting training and test input data")
            #splitting the data into features and target removing the last column
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )

            models = {
                'Random Forest': RandomForestRegressor(),
                'Decision Tree': DecisionTreeRegressor(),
                'Gradient Boosting': GradientBoostingRegressor(),
                'Linear Regression': LinearRegression(),
                'XGBRegressor': xgboost.XGBRegressor(),
                'CatBoosting Regressor': catboost.CatBoostRegressor(verbose=False),
                'AdaBoost Regressor': AdaBoostRegressor(),
                'K-Neighbors Regressor': KNeighborsRegressor()
            }

            params = {
                'Decision Tree': {
                    'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    'splitter': ['best', 'random'],
                    'max_features': ['sqrt', 'log2']

                },
                'Random Forest': {
                    'n_estimators': [8, 16, 32, 64, 128, 256],
                    # 'max_features': ['sqrt', 'log2'],
                    # 'max_depth': [None, 10, 20, 30, 40, 50],
                    # 'min_samples_split': [2, 5, 10],
                    # 'min_samples_leaf': [1, 2, 4]
                },
                'Gradient Boosting': {
                    # 'loss': ['squared_error', 'absolute_error', 'huber', 'quantile'],
                    'learning_rate': [0.1, 0.01, 0.05, 0.001],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                'Linear Regression': {},
                'K-Neighbors Regressor': {
                    'n_neighbors': [3, 5, 7, 9, 11],
                    # 'weights': ['uniform', 'distance'],
                    # 'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']
                },
                'XGBRegressor': {
                    'learning_rate': [0.1, 0.01, 0.05, 0.001],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                'CatBoosting Regressor': {
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [30, 50, 100]
                },
                'AdaBoost Regressor': {
                    'learning_rate': [0.1, 0.01, 0.5, 0.001],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                }
            }

            model_report:dict = evaluate_models(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, models=models, params=params)
            
            #to get the best model score from the model_report
            best_model_score = max(sorted(model_report.values()))
            
            #to get the best model name from the model_report
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]
            
            if best_model_score < 0.6:
                raise CustomException("No best model found")
            
            logging.info(f"Best found model on both training and testing dataset {best_model_name} with r2 score {best_model_score}")
            
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            return best_model_name

        except Exception as e:  
            raise CustomException(e, sys)


            