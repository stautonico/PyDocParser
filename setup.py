import pathlib
from setuptools import setup, find_packages
import pydocparser

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()


def calculate_install_requires():
    with open('requirements.txt') as f:
        lines = f.read().splitlines()

    # Clear empty lines or comments
    return [line for line in lines if line and not line.startswith('#')]


setup(
    name='PyDocParser',
    version=pydocparser.__version__,
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/stautonico/pydocparser',
    license='MIT',
    author='Steve Tautonico',
    author_email='stautonico@gmail.com',
    description='An unofficial python client for the DocParser API',
    long_description=README,
    install_requires=calculate_install_requires(),
    keywords=["docparser", "API", "Wrapper"],
    long_description_content_type="text/markdown"

)
