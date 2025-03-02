#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='robopost-client',
    version='0.0.1',
    description='Robopost Client',
    long_description=readme,
    license='MIT',
    author='Robopost',
    author_email='support@robopost.app',
    url='',
    packages=['robopost_client'],
    install_requires=['requests==2.32.3', 'urllib3==2.2.3', 'pydantic==2.10.3'],
    entry_points={
        'console_scripts': [
            'robopost = robopost_client.robopost_cli:main',
        ],
    },
)
