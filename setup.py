from setuptools import setup

import sys


setup(
    name = 'tricli',
    version = "2.1.0", 
    author = "Anish Lakkapragada", 
    author_email="anish.lakkapragada@gmail.com",
    description = "tricli manages a trie data structure that can be globally accessed.", 
    keywords=["REST", "Data Structures", "Trie"], 
    packages = ['tricli'],
    license = "MIT", 
    entry_points = {
        'console_scripts': [
            'tricli = tricli.__main__:main'
        ]
    })
