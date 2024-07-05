from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="myproject",
    version="0.0.1",
    author="mohit gupta",
    author_email="cse.mohitgupta.07@gmail.com",
    description="Library for pdf to json convertor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mohitgupta07/pdf_to_json_extractor",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
