import os

from setuptools import setup, find_packages

def get_long_desc():
    with open("README.md", "r") as readme:
        desc = readme.read()
    return desc

def setup_package():
    setup(
        name='chord',
        version='0.1.0',
        description='CLI Client for ToyChord API',
        long_description=get_long_desc(),
        url='https://github.com/fillmln/ToyChord',
        license='MIT',
        long_description_content_type='text/markdown',
        packages=find_packages(),
        install_requires=[],
        entry_points = {
            'console_scripts': [
                'chord=cli.__main__:cli',
            ],
        },
        classifiers=[
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3'
        ],
        author = 'Britney Spears',
        author_email = 'struck_a_chord@chord.toy'
    )

if __name__ == '__main__':
    setup_package()
