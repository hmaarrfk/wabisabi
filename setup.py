#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages


# Loads _version.py module without importing the whole package.
def get_version_and_cmdclass(pkg_path):
    import os
    from importlib.util import module_from_spec, spec_from_file_location
    spec = spec_from_file_location(
        'version', os.path.join(pkg_path, '_version.py'),
    )
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.__version__, module.get_cmdclass(pkg_path)


version, cmdclass = get_version_and_cmdclass('wabisabi')


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()


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
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    description=(
        "Deprecate your code effortlessly with decorators. "
        "Give useful warnings and docstrings for different deprecations."
    ),
    license="BSD license",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='deprecation factory wabisabi',
    name='wabisabi',
    packages=find_packages(include=['wabisabi']),
    install_requires=['packaging'],
    python_requires=">=3.8",
    setup_requires=['setuptools'],
    tests_require=test_requirements,
    url='https://github.com/hmaarrfk/wabisabi',
    version=version,
    cmdclass=cmdclass,
    zip_safe=False,
)
