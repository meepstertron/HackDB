from setuptools import setup, find_packages

setup(
    name="HackDB",  # Replace with your package name
    version="0.0.2",  # Match your client version
    author="Jan Koch",
    author_email="meepstertron@gmail.com",
    description="A Python client for interacting with HackDB.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/meepstertron/HackDB",  
    packages=find_packages(where="lib/python"),
    package_dir={"": "lib/python"},
    install_requires=[
        "requests>=2.25.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)