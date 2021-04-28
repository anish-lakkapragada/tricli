from setuptools import setup

import sys

version_name = sys.argv[1].replace("refs/tags/", "")
del sys.argv[1]

with open("CLI_README.md", "r") as fh:
    read_me_description = fh.read()


setup(
    name = 'tricli',
    version=version_name, 
    author = "Anish Lakkapragada", 
    author_email="anish.lakkapragada@gmail.com",
    description = "tricli manages a trie data structure that can be globally accessed.", 
    keywords=["REST", "Data Structures", "Trie"], 
    packages = ['tricli'],
    license = "MIT", 
    long_description = read_me_description, 
    long_description_content_type="text/markdown",
    entry_points = {
        'console_scripts': [
            'tricli = tricli.__main__:main'
        ]
    })
