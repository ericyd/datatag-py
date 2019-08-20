# https://packaging.python.org/tutorials/packaging-projects/
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="inclusion",
    version="0.1.0",
    author="Eric Dauenhauer",
    author_email="eric@ericyd.com",
    description="Package for fast set intersection on datasets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ericyd/inclusion-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
