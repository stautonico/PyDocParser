![DocParser Logo](https://github.com/tman540/PyDocParser/blob/master/img/logo.png?raw=true)

## Unofficial python client for the Docparser API



#### Table Of Contents

* [Installation](#Installation)
* [Usage](#Usage)
* [Contributing](#Contributing)
* [License](#License)
* [Changelog](#Changelog)
* [To-Do](#To-Do)
* [Documentation](https://github.com/tman540/PyDocParser/blob/master/docs/PyDocParser%20Documentation.md)

<br>

#### Installation

**__Installation for general usage__**:

**Note:** pydocparser was only tested for python3 (not guaranteed to work for [python2](https://www.jetbrains.com/research/python-developers-survey-2018/))

`pip install pydocparser` or if you have python3 `pip3 install pydocparser`

**OR**

You can download the release of your choice from [here](https://github.com/tman540/PyDocParser/releases)

Unzip the file

change directory to the unziped folder

run `python setup.py install` or `python3 setup.py install`

<br>

__**Installation for development:**__

`git clone https://github.com/tman540/pydocparser`

`pip install -r requirements.txt`



#### Usage

To use pydocparser, you must create an instance of the `Parser` class from the `pydocparser` module:

```python
import pydocparser

parser = pydocparser.Parser()
```

Next, you must obtain your secret API key (which you can get from [here](https://app.docparser.com/myaccount/api))

Now, pydocparser requires this key to be able to access your account. You can do that like this:

```python
parser.login(YOUR_API_KEY_HERE)
```

The docparser API has a function for testing connection to the API

```python3
result = parser.ping()
print(result)
# pong
```

If `parser.ping()` returns ‘pong’, then you have a successful connection to the docparser API. If you get an output like this: `Invalid API key. Use Parser.login(api_key)` and you entered your API key, make sure your API key is correct.

You can get a list of current parsers like this:

```python
parsers = parser.get_parsers()
```

This will return a list of the names of all available parsers.

To upload a file to docparser, you can use the `upload` function:

```python
id = parser.upload("fileone.pdf", "PDF Parser") #ars: file to upload, the name of the parser
```

The function will return the document ID of the file that was just uploaded. To retrieve the parsed data, you can call the `fetch` function:

```python
data = parser.fetch("PDF Parser", id) # The id is the doc id that was returned by `parser.upload()`
```

`fetch` returns all the parsed data from the file you selected

<br>

#### Contributing

This project started from the need to use docparser through python at work. I noticed that there was no API library for python, so I decided to make it myself. I am a one man operation so I am glad to accept any help I can get. You can contribute by making your changes, submitting a pull request with a detailed description of what you added. I will review your changes, and if I decide that your changes will make it into the next release, I will credit you accordingly. You can also contribute by submitting bug reports/feature request through GitHub issues.

<br>

#### License

This library is available as open source un the [MIT License](https://github.com/tman540/PyDocParser/blob/master/LICENSE.md).

<br>

#### Changelog

V1.0 (7/11/19) Initial release

[V1.1 (7/12/19) Bug Fixes + New Functions](https://docparser.tautonico.tech/changelog)
<br>

#### To-Do

- [ ] Change function names to more closely resemble those in the PHP/Node/AJAX clients
- [x] Update setup.py to include install requirements
- [X] Fix README.md to work better on [PyPi](https://pypi.org/project/PyDocParser/)
