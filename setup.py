from setuptools import setup
from setuptools import find_packages

setup(
    name='python_utilities',
    version='1.0',
    packages=find_packages(),
    url='',
    license='',
    author='Samuel Beland-Leblanc',
    author_email='samuel.beland.leblanc@gmail.com',
    description='Different pyhton utility modules',
    install_requires=[
        'lxml',
        'numpy'
    ]
)
