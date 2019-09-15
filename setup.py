# https://packaging.python.org/tutorials/packaging-projects/
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="datatag",
    version="1.0.0",
    author="Eric Dauenhauer",
    author_email="eric@ericyd.com",
    description="Lightweight, flexible data tagging and querying",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ericyd/datatag-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
