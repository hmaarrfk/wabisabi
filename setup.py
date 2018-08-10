#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
import versioneer

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = ['pytest', 'numpydoc']

setup(
    author="Mark Harfouche",
    author_email='mark.harfouche@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Python deprecation factory ensuring useful warnings and docstrings for different deprecations.",
    install_requires=requirements,
    license="BSD license",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='deprecation_factory',
    name='deprecation_factory',
    packages=find_packages(include=['deprecation_factory']),
    setup_requires=['setuptools'],
    tests_require=test_requirements,
    url='https://github.com/hmaarrfk/deprecation_factory',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    zip_safe=False,
)
