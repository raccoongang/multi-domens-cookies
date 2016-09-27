import os
from os.path import join, dirname, split
from setuptools import setup, find_packages


with open('requirements.txt', 'r') as f:
    requirements = f.readlines()


setup(
    name='multi_domens_cookies',
    version='1.0',
    description='multi-domen-cookies for auth on edx',
    author='dorosh',
    url='https://github.com/raccoongang/multi-domens-cookies',
    
    install_requires=requirements,
    packages=find_packages(exclude=['tests']),
)
