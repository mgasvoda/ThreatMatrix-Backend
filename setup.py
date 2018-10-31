import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="threatmatrix_backend",
    version="0.0.1",
    author="Michael Gasvoda",
    description="Conflict data aggregation and analysis framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mgasvoda/ThreatMatrix",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests>=2.18.4', 
        'sqlalchemy>=1.2.7',
        'pandas>=0.23.0',
        'numpy>=1.14.3'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ]
)