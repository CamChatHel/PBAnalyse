from setuptools import setup, find_packages

setup(
    name='Tool_Pruefbericht_Daten_V2.0',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        line.strip() for line in open('requirements.txt').readlines()
    ],
)
