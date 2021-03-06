#!/usr/bin/env python
from setuptools import setup, find_packages
import sys
import subprocess
import os

# Update version from latest git tags.
# Create a version file in the root directory
version_py = os.path.join(os.path.dirname(__file__), 'ngt_archive/version.py')
try:
    git_describe = subprocess.check_output(["git", "describe", "--tags"]).rstrip().decode('utf-8')
    version_msg = "# Managed by setup.py via git tags.  **** DO NOT EDIT ****"
    with open(version_py, 'w') as f:
        f.write(version_msg + os.linesep + "__version__='" + git_describe.split("-")[0] + "'")
        f.write(os.linesep + "__release__='" + git_describe + "'" + os.linesep)

except Exception as e:
    # If there is an exception, this means that git is not available
    # We will used the existing version.py file
    pass

try:
    with open(version_py) as f:
        code = compile(f.read(), version_py, 'exec')
        exec(code)
except:
    __release__=None

packages = find_packages(exclude=["*.tests",])

if sys.version_info < (2,6):
    sys.exit('Sorry, Python < 2.6 is not supported')
elif sys.version_info < (2,7):
    sys.exit('Sorry, Python < 2.7 is not supported')

setup(name='ngt_archive',
      version=__release__,
      description='NGEE Tropics Archive Service',
      author='Val Hendrix',
      author_email='vchendrix@lbl.gov',
      packages = packages,
      py_modules = ['manage'],
      include_package_data=True,
      install_requires=[
            "django >= 1.8, < 2.0",
            "djangorestframework == 3.4.3",
            "django-filter ==  0.13.0",
            "django-daterange-filter == 1.3.0",
            "pyldap",
            "django-auth-ldap == 1.2.8"
      ]
     )
