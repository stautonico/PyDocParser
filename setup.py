from setuptools import setup

setup(
    name='PyDocParser',
    version='1.0',
    packages=['pydocparser'],
    url='https://github.com/tman540/pydocparser',
    license='MIT',
    author='Steve Tautonico',
    author_email='stautonico@gmail.com',
    description='A python client for the DocParser API',
    long_description=open("README.md").read(),
	install_requires=["requests>=2.22.0"],
	keywords=["docparser", "API",],
	long_description_content_type="text/markdown"
	
)
