import os
from setuptools import setup, find_namespace_packages

# Read version from version.py
version = {}
with open(os.path.join("src", "version.py"), encoding="utf-8") as f:
    exec(f.read(), version)

# Read README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mkdocs-sql",
    version=version["__version__"],
    author="Vishal Gandhi",
    description="A MkDocs plugin for embedding output of SQL queries in your documentation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ivishalgandhi/mkdocs-sql",
    package_dir={"mkdocs_sql": "src"},
    packages=["mkdocs_sql"],
    include_package_data=True,
    install_requires=[
        "mkdocs>=1.6.1",
        "pandas>=2.2.3",
        "tabulate>=0.9.0",
        "pyyaml>=6.0.2"
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
