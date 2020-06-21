# coding: utf-8

"""
    Meta-Templating
    TODO
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "meta-templating-engine"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["TODO"]

setup(
    name=NAME,
    version=VERSION,
    description="meta-templating engine for svgs",
    author="TODO",
    author_email="TODO",
    url="TODO",
    keywords=["TODO"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests", "test-assets"]),
    include_package_data=True,
    license="AGPLv3",
    long_description="""\
    TODO
    """
)
