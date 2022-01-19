# -*- coding: utf-8 -*-
from __future__ import division

import pathlib
import sys

sys.path.insert(0, '.')
sys.path.insert(0, 'eufrates')
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(name='eufrates',
      version='1.0',
      description='A workflow framework and BPMN/BRS/DMN Processor',
      long_description=README,
      long_description_content_type="text/markdown",
      author='Multix',
      author_email='contact@multix.tech',
      license='lGPLv3',
      packages=find_packages(exclude=['tests', 'tests.*']),
      install_requires=['future', 'configparser', 'lxml', 'celery', 'dateparser', 'pytz'],
      keywords='eufrates workflow bpmn engine',
      url='https://github.com/joaquim-mattos-dev/eufrates',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPLv3)',
          'Programming Language :: Python',
          'Topic :: Other/Nonlisted Topic',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ])
