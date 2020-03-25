import io
import os

from setuptools import find_packages, setup

# Package meta-data.
NAME = "sushi"
DESCRIPTION = "Minimalist secrets management in Python"
URL = "https://github.com/alexmacniven/sushi"
EMAIL = "macniven.ap@gmail.com"
AUTHOR = "Alex Macniven"
REQUIRES_PYTHON = ">=3.7.0"
VERSION = "0.0.1-beta.1"

# What packages are required for this module to be executed?
REQUIRED = [

]

# What packages are optional?
EXTRAS = {
    "dev": [
        "pytest",
        "pytest-mock",
        "rope",
        "flake8",
        "coverage",
    ]
}

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if "README.md" is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package"s __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION

setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(
        exclude=["tests", "*.tests", "*.tests.*", "tests.*"]
    ),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license="NONE"
)
