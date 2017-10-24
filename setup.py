#! /usr/bin/env python3
import os
import shutil
import sys
from setuptools import setup, find_packages

VERSION = '0.0.0a1'

long_description = '''DORA long description'''

excluded = []
def exclude_package(pkg):
    for exclude in excluded:
        if pkg.startswith(exclude):
            return True
    return False

def create_package_list(base_package):
    return ([base_package] +
            [base_package + '.' + pkg
             for pkg
             in find_packages(base_package)
             if not exclude_package(pkg)])

setup_info = dict(
    # Metadata
    name='dora',
    version=VERSION,
    #author='Alex Holkner',
    #author_email='Alex.Holkner@gmail.com',
    #url='http://pyglet.readthedocs.org/en/latest/',
    #download_url='http://pypi.python.org/pypi/pyglet',
    #description='Cross-platform windowing and multimedia library',
    long_description=long_description,
    #license='BSD',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        #'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    # Package info
    packages=create_package_list('dora'),

    # Add _ prefix to the names of temporary build dirs
    options={
        'build': {'build_base': '_build'},
        #        'sdist': {'dist_dir': '_dist'},
    },
)

setup(**setup_info)

if __name__ == '__main__':
	print('Hello world!')
