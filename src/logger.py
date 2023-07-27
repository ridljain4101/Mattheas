import logging
import os
from datetime import datetime

LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
##f string is used in place when placeholders are used but we don't want to use .format ahead.
logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE)
os.makedirs(logs_path,exist_ok=True)
##exist_ok:true, even though there is a similiar file,keep updating it.

LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)


##overriding logging functionality
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    ##info: used to record messages/operations occuring in the script regularly.
)



