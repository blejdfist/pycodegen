# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='pycodegen',
    version='0.0.1',
    description='Code generator written in Python',
    url='https://github.com/blejdfist/pycodegen',
    python_requires='>=3.4',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['pycodegen=pycodegen.cli:main']
    },
    install_requires=[
        'jinja2>=2.10'
    ],
    extras_require={
        'CPP': ["clang>=5.0"]
    },
    setup_requires=["pytest-runner"],
    tests_require=["pytest"]
)

