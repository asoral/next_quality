# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in next_quality/__init__.py
from next_quality import __version__ as version

setup(
	name='next_quality',
	version=version,
	description='Module',
	author='Dexciss Technology',
	author_email='dexciss@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
