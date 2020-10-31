"""Installation script."""
from pathlib import Path
from setuptools import setup, find_packages

DESCRIPTION = "ZomPixel"
APP_ROOT = Path(__file__).parent
README = (APP_ROOT / "README.md").read_text()
AUTHOR = "Thibault, Romain -> images Ethan -> Code"
AUTHOR_EMAIL = "N/A"
PROJECT_URLS = {
    "Documentation": "N/A",
    "Bug Tracker": "N/A",
    "Source Code": "Where you find it !",
}
INSTALL_REQUIRES = [
    "pygame",
    "rethinkdb",
]
EXTRAS_REQUIRE = {
    "dev": [
        "black",
        "flake8",
    ]
}

setup(
    name="zompixel",
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    version="0.1",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    license="MIT",
    url=PROJECT_URLS["Source Code"],
    project_urls=PROJECT_URLS,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
)
