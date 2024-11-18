from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mkdocs-sql",
    version="0.1.0",
    author="Vishal Gandhi",
    description="A MkDocs plugin for executing and embedding output of SQL queries in your documentation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ivishalgandhi/mkdocs-sql",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "mkdocs>=1.5.0",
        "pandas>=1.0.0",
        "tabulate>=0.8.0",
        "pyyaml>=5.1"
    ],
    entry_points={
        'mkdocs.plugins': [
            'sql = mkdocs_sql.plugin:SQLPlugin',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: MkDocs",
        "Topic :: Documentation",
        "Topic :: Database",
    ],
    python_requires=">=3.7",
)
