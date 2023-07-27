from setuptools import find_packages,setup
from typing import List    

HYPEN_E_DOT = '-e .'
def get_requirements(file_path:str)->List[str]:
    requirements=[]
    with open(file_path) as file_obj:
         requirements=file_obj.readlines()
         requirements=[req.replace("\n","") for req in requirements]
    ## just read the lines in the requirements.txt and then since for every new line /n occurs, replaced it.

         if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
        ##since while implementing this we might get -e. while reading the lines from requirements.txt
        
    return requirements

##this function return a list of requirements

setup(
name = 'performance_prediction_model',
version='0.0.1',
author = 'Ridhim',
author_email='ridhimjain41001@gmail.com',
packages=find_packages(),
install_requires=get_requirements('requirements.txt')
## function used to import as many libraries as required later on.

)