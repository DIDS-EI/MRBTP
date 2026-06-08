from setuptools import setup, find_packages
import os

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='mabtpg',
    version='0.0.1',
    packages=['mabtpg'],
    install_requires=required,
    author='',
    author_email='',
    description='Efficient Multi-Robot Behavior Tree Planning and Collaboration',
    url='',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

