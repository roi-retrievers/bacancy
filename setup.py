from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in bacancy/__init__.py
from bacancy import __version__ as version

setup(
	name="bacancy",
	version=version,
	description="Customizations to ERPNext for Bacancy Systems",
	author="ROI Retrievers",
	author_email="roiretrievers@gmail.com​",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
