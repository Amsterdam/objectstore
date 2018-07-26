#!/usr/bin/env python

import sys

import codecs

from setuptools import setup
from setuptools.command.test import test as TestCommand


# https://docs.pytest.org/en/latest/goodpractices.html

class PyTest(TestCommand):
    """ Custom class to avoid depending on pytest-runner.
    """
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['--cov', 'objectstore']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

version = '2018.7.25'

packages = ['objectstore']

requires = [
    'python-swiftclient',
    'datapunt-config-loader',
    'python-keystoneclient',
]

requires_test = [
    'pytest',
    'pytest-cov',
]

requires_extras = {
    'docs': [
        'sphinx',
        'sphinx-autobuild',
        'sphinx-rtd-theme',
    ],
    'dev': requires_test + ['pylint', 'twine'],
}

setup(
    name='datapunt-objectstore',
    version=version,
    description='Datapunt Amsterdam objectstore module',
    long_description=long_description,
    url='https://github.com/amsterdam/objectstore',
    author='Datapunt Amsterdam',
    author_email='datapunt@amsterdam.nl',
    license='Mozilla Public License Version 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
    ],
    cmdclass={'test': PyTest},
    packages=packages,
    install_requires=requires,
    tests_require=requires_test,
    extras_require=requires_extras,
    setup_requires=['flake8'],
)
