from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='RoboBurp2',
    version='1.1',
    packages=['roboburp2'],
    # package_dir={'': 'roboburp2'},
    url='https://www.github.com/we45/RoboBurp2',
    license='MIT',
    author='we45',
    author_email='info@we45.com',
    description='Robot Framework Library for the BurpSuite Pro Vulnerability Scanner',
    install_requires=[
        'requests',
        'robotframework==3.0.4'
    ],
    long_description = long_description,
    long_description_content_type='text/markdown',
    include_package_data=True
)
