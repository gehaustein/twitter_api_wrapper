import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

def read_requirements():
    return [l.strip() for l in open("requirements.txt").readlines()]

read_requirements()

DESCRIPTION = 'A wrapper for executing simple commands with Tweepy'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=read_requirements(),
      python_requires='>3.9.0'
)
