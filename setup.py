#resopoonsible for creating packages of this machine learning project

from setuptools import find_packages,setup
from typing import List

def get_requirements(file_path:str)->list[str]:
    '''
    this function will return the list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]
        if "-e ." in requirements:
            requirements.remove("-e .")
    return requirements
    #this will automatically trigger setup.py


setup(
    name="mlproject",
    version="0.0.1",
    author="Parth",
    author_email="parthshethji2693@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)
