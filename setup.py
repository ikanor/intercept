#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup


setup(
    name='intercept',
    description='Capture your exceptions with a decorator.',
    maintainer='Franky Rodriguez',
    maintainer_email='prados@gmail.com',
    version='0.1.2',
    url='https://github.com/ikanor/interceptor',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],
    packages=find_packages(exclude=['docs', 'tests*'])
)
