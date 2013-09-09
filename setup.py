import os

from setuptools import setup, find_packages
from postmaster.version import VERSION

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()


requires = [
]

setup(name='postmaster',
      version=VERSION,
      description='Library for postmaster.io service',
      long_description=README,
      author='Postmaster',
      author_email='support@postmaster.com',
      url='http://postmaster.io',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='test',
      install_requires=requires,
      )

