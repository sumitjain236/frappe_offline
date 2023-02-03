from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in frappe_offline/__init__.py
from frappe_offline import __version__ as version

setup(
	name="frappe_offline",
	version=version,
	description="Store Data locally and sync with frappe",
	author="Sumit Jain",
	author_email="sumit@example.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
