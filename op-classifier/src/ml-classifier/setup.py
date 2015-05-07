from distutils.core import setup
from setuptools import setup
from setuptools.command.install import install
import os
import sys

class CustomInstallCommand(install):
    """Customized setuptools install command - prints a friendly greeting."""
    def run(self):
        print "Installing libsvm first"
        os.chdir('src/ml2/algs/libsvm-3.1')
        os.system('make clean')
        os.system('make all')
        print "End of libsvm installation"
        os.chdir('../../../..')
        install.run(self)


setup(
	cmdclass={
        'install': CustomInstallCommand,
    },
	name = 'ml-classifier',
	version = '1.0',
	packages = ['ml2'],
        package_dir = {'ml2': 'src/ml2' },
	package_data = {'ml2': ['scripts/classifier', 'scripts/xvalidator', 'algs/libsvm-3.1/svm-train',
                                'algs/libsvm-3.1/svm-predict',
                                'algs/libsvm-3.1/svm-scale'], },
	#package_data = {'ml2': ['default_hermesrc']},
	
	# project metadata
	author = 'Faiyaz Zamal',
	author_email = 'faiyaz.zamal@mail.mcgill.ca',
	description = 'A system for inferring demographics for Twitter users.'
        license = 'BSD',
	#url = 'http://www.networkdynamics.org',
)
