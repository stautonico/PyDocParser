import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='PyDocParser',
    version='1.1.2.1',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/tman540/pydocparser',
    license='MIT',
    author='Steve Tautonico',
    author_email='stautonico@gmail.com',
    description='A python client for the DocParser API',
    long_description=README,
    install_requires=["requests>=2.22.0"],
    keywords=["docparser", "API"],
    long_description_content_type="text/markdown"

)
