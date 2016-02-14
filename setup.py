#!/usr/bin/python3

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='smtracker',
    version='1.0.1',
    description='A StepMania score tracker',
    long_description=long_description,
    url='https://github.com/japareaggae/smtracker-python',
    author='Renan Guilherme Lebre Ramos',
    author_email='japareaggae@gmail.com',
    license='GPLv3+',
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3'
        ],
    packages=find_packages(),
    entry_points={
        'gui_scripts':
            ['smtracker = smtracker.smtracker:main']
        },
)
