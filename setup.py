import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

requires = [
]

setup(name='postmaster-python',
      version='0.0',
      description='Library for postmaster.io service',
      long_description=README,
      classifiers=[
        "Programming Language :: Python",
        ],
      author='',
      author_email='',
      url='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='test',
      install_requires=requires,
      entry_points="""\
      """,
      )

