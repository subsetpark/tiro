from setuptools import setup, find_packages

setup(
    name="Abba",
    version="0.1",
    description="An abbreviation engine.",
    url="http://github.com/subsetpark/abba",
    author="Zach Smith",
    author_email="zd@zdsmith.com",
    packages=find_packages(),
    package_data={'mypkg': ['tna.ini']}
)
