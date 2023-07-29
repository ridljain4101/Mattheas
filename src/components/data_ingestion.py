import os 
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_transform import DataTransformation
from src.components.data_transform import DataTransformConfig

@dataclass ##helps in directly defining the class rather than going for the constructor.
class DataIngestionConfig:##any input that is required is given through here.
    train_data_path:str=os.path.join("artifacts","train.csv")
    ##here providing the initial path to the data ingestion-> output saves the data in the artifact file.
    test_data_path:str=os.path.join("artifacts","test.csv")
    raw_data_path:str=os.path.join("artifacts","data.csv")


class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()
    

    def initiate_data_ingestion(self):##function used to read the data from the database
        logging.info("Entered the data ingestion method or component")
    ##error catching now
        try:
            df=pd.read_csv('notebook\data\stud.csv')
            logging.info("read the data as a dframe")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
        ##making a folder with the path as of the training data in the artifact folder.--creation of artifacts folder

            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
        ##saving the data as a csv to the raw data path, which is based inside off the artifact folder created above
            logging.info("train test split initiation")
            train_set,test_set = train_test_split(df,test_size=0.25,random_state=42)
        ##save train and test as csv to corresponding paths mentioned above
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("ingestion of data completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            ##returned to process further for data transformation
            )




        except Exception as e:
            raise CustomException(e,sys)





if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()##this data is passed onto the DT for DATA TRANSFORMATION.

    data_transformation=DataTransformation()
    data_transformation.initiate_data_transformation(train_data,test_data)



        
 



