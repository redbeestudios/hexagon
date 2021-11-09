from pathlib import Path

from setuptools import setup, find_packages
from pipenv_setup.lockfile_parser import get_default_packages, format_remote_package

# esto se actualiza solo con https://python-semantic-release.readthedocs.io/en/latest/index.html
__version__ = "0.21.0"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

local_packages, remote_packages = get_default_packages(Path("Pipfile.lock"))

setup(
    name="hexagon",
    version=__version__,
    author="Joaco Campero",
    author_email="joaquin@redbee.io",
    description="Una CLI para generar CLIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/redbeestudios/hexagon",
    project_urls={"Bug Tracker": "https://github.com/redbeestudios/hexagon/issues"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=["tests", "tests.*", "e2e", "e2e.*"]),
    package_data={"": ["*.md"]},
    install_requires=[
        v
        for k, v in [
            format_remote_package(name, config)
            for name, config in remote_packages.items()
        ]
    ],
    python_requires=">=3.7",
    entry_points="""
        [console_scripts]
        hexagon=hexagon.__main__:main
    """,
    platform="debian",
)
