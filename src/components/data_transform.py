import sys
from dataclasses import dataclass
import os

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


@dataclass
class DataTransformConfig:
    preprocessor_obj_file_path =os.path.join("artifacts","preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformConfig()


    def get_data_transformer_object(self):
        ##making pkl files used to convert cat->num,OHE,etc.:actual data transformation occurs here.
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]
 ##pipelines creation
            num_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ]
            )

            cat_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("OHE",OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )
            logging.info("Numerical cols Stnd scaling and cat cols OHE done")

            preprocessor=ColumnTransformer(
                [##comb. both cat and num ppls.
                    ("num_ppl",num_pipeline,numerical_columns),
                    ("cat_ppl",cat_pipeline,categorical_columns)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)

##running the DT created above over the train,test data
    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            logging.info("#1 : reading train,test data")

            logging.info("#2 : getting the preprocessor object")
            preprocessing_obj=self.get_data_transformer_object()##from the above created function which returns the preprocessor.


            target_column_name="math_score"
            numerical_columns=["writing_score", "reading_score"]

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)##X: for train
            target_feature_train_df=train_df[target_column_name]
            logging.info("#3 : prepping train into indep and dep.")

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)##X:for test
            target_feature_test_df=test_df[target_column_name]

            logging.info(
                f"#4  : Applying preprocessing object on training dataframe and testing dataframe inputs"
            )
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[ 
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            logging.info(f"concatenating the processed input and the output data.")

##saving the object in the Hard disk.
            save_object(
    ##refer:utils
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )
            logging.info(f"saved the processed object and the file path")


            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e,sys)



