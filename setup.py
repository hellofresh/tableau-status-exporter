from setuptools import setup
from setuptools import find_packages

NAME = "tableau-exporter"

VERSION = "0.2.0"

REQUIRES = [
    "pyyaml",
    "requests",
    "prometheus_client",
    "twisted"
]

setup(
    name=NAME,
    version=VERSION,
    url="https://github.com/hellofresh/tableau-status-exporter",
    author="Zsolt Toth",
    author_email="zt@hellofresh.com",
    description="Prometheus exporter to expose status of Tableau Server processes",
    long_description=open('README.md').read(),
    package_data={'': ['*.yml']},
    packages=find_packages(),
    install_requires=REQUIRES,
)
