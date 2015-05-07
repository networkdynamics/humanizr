#from distutils.core import setup
from setuptools import setup

setup(
    name = 'Humanizr',
    url = 'http://networkdynamics.org/resources/software/humanizr',
    license = 'BSD',
    version = '1.0.0',
    packages = ['op-classifier'],
    package_dir = {'op-classifier': 'op-classifier'},
    install_requires = ['python-cjson'],
    author = 'James McCorriston',
    author_email = 'james.mccorriston@mail.mcgill.ca',
    description = 'A tool for classifying Twitter users as Organizations or Personal accounts. Includes feature extraction and SVM classification.'
)

