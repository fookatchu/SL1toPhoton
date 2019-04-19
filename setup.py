#!venv/Scripts/python

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='SL1oPhoton',
      version='0.1',
      # packages=['pyphotonfile'],
      author="Heiko Westermann",
      author_email="heiko+sl1tophoton@orgizm.net",
      description="Tool for converting Slic3r PE's SL1 files to Photon files for the Anycubic Photon 3D-Printer",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/fookatchu/SL1toPhoton",
      packages=find_packages(),
      install_requires=['pyphotonfile'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
      ],
     )
