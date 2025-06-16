from setuptools import setup

setup(
    name='hackdb-cli',
    description='Command line interface for HackDB',
    version='0.1',
    py_modules=['main'],
    entry_points={
        'console_scripts': [
            'hackdb = main:main',
        ],
    },
    install_requires=[
        'requests',
        'setuptools',
        'uuid'
    ],
)