import re
from setuptools import setup, find_packages


description_long = """
System Information
------------------
Hardware
    Processor
Python
    Version
    Compiler
System
    Processor
        Type
        Cores
    Memory
        Installed
        Available
    OS
    Release
    Machine
    Architecture
    Hostname
    Username
"""


# Retrieve version number
VERSIONFILE = "envinfo/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE))


setup(
    name='envinfo',
    version=verstr,
    packages=find_packages,
    install_requires=[
        'platform',
        'psutil',
        'multiprocess'
    ],
    url='https://github.com/mrstephenneal/envinfo',
    license='GPL-3.0',
    author='Stephen Neal',
    author_email='stephen@stephenneal.net',
    description='A lightweight utility for retrieving system information and specifications.',
    description_long=description_long
)
