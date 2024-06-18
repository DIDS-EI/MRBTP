from setuptools import setup, find_packages
import os

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='mabtpg',
    version='0.0.1',
    packages=['mabtpg'],
    install_requires=required,
    author='DIDS-EI',
    author_email='dids_ei@163.com',
    description='A Platform for Multi-Agent Behavior Tree Planning and Evaluation',
    url='https://github.com/DIDS-EI/BTGym',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

