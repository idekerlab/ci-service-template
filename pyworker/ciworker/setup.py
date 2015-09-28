# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='ciworker',
    version='0.1.3',
    description='Cytoscape CI base service template',
    long_description='Template worker code for Cytoscape CI.',
    author='Keiichiro Ono',
    author_email='kono@ucsd.edu',
    url='https://github.com/idekerlab',
    license='MIT License',
    keywords=['graph', 'network', 'cytoscape'],
    install_requires=[
        'requests',
        'pyzmq',
        'redis'
    ],
    classifiers=[
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    test_suite='tests',
    packages=find_packages(),
    include_package_data=True,
)
