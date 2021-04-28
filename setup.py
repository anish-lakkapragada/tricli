from setuptools import setup

import sys

version_name = sys.argv[1].replace("refs/tags/", "")
del sys.argv[1]


setup(
    name = 'tricli',
    version = version_name, 
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
