# coding: utf-8

"""
    RiseML API


    OpenAPI spec version: 1.1.0
    Contact: support@riseml.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import sys
from setuptools import setup, find_packages

NAME = "riseml"
VERSION = "0.2.0"


REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]

REQUIRES += ['pyyaml', 'requests']

setup(
    name=NAME,
    version=VERSION,
    description="RiseML API client",
    author_email="support@riseml.com",
    url="",
    keywords=["RiseML"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    
    """
)

