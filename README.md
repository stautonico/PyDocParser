![DocParser Logo](https://github.com/stautonico/PyDocParser/blob/master/img/logo.png?raw=true)

## Unofficial Python Client for the Docparser API

### Table of Contents

* [Installation](#Installation)
* [Usage](#Usage)
* [Contributing](#Contributing)
* [License](#License)
* [Changelog](#Changelog)
* [To-Do](#To-Do)
* [Documentation](https://docparser.tautonico.tech/docs)
* [Additional Information](#Additional-Information)

<br>

### Installation

**Important Note:** PyDocParser does not support Python 2.X. **The minimum compatible version is Python 3.8.**

#### Install with pip

`pip install pydocparser`

#### Install from Source

1. Download the release of your choice from [here](https://github.com/stautonico/PyDocParser/releases)
2. Unzip the file (`unzip PyDocParser-<version>.zip` or use your favorite archive manager)
3. Change directory to the unzipped folder (`cd PyDocParser-<version>`)
4. Run `python setup.py install`

#### Install for Development

1. Clone the repository (`git clone https://github.com/stautonico/pydocparser`)
2. (Optional, but recommended) Create a virtual environment (`python -m venv venv`)
3. Activate the virtual environment (`source venv/bin/activate`)
4. Install the dependencies (`pip install -r requirements.txt`)

<br>

### Usage

This is a basic example of how to use PyDocParser. For more examples, check out
the [documentation](https://docparser.tautonico.tech/docs).

The first thing you need to do is create an instance of the `Docparser` class from the `pydocparser` module, and
call the `login()` method, passing your API key as an argument:

```python
import pydocparser

parser = pydocparser.Docparser()

login_result = parser.login("your_api_key")  # returns True if successful, False otherwise
```

Next, you can upload a document to a parser. This example uploads a local file using the `upload_local_file_by_path()`
method, providing the path to the file and the label of the parser as arguments:

```python
try:
    document_id = parser.upload_local_file_by_path("path/to/file.pdf", "parser_label")
except Exception as e:
    print("Something went wrong while uploading the file")
    print(e)
    exit(1)

print(document_id)  # The ID of the document in the parser if uploading was successful
```

Finally, you can retrieve the parsed data using the `get_one_result()` and providing the parser label and the document
ID as arguments:

```python
try:
    result = parser.get_one_result("parser_label", document_id)
except Exception as e:
    print("Something went wrong while retrieving the parsed data")
    print(e)
    exit(1)

print(result)  # The parsed data if retrieval was successful (an array of dictionaries)
```

To view a full list of the available methods, check out the [documentation](https://docparser.tautonico.tech/docs).

### Contributing

Thank you for considering contributing to **PyDocParser**. We appreciate your interest and support in making this
project
better.

There aren't many guidelines for contributing to this project, but there are a few simple rules:

- Be respectful towards other contributors and maintainers.
- Make sure your code is clean and well-documented.
- Write clear commit messages and include relevant information.
- Be civil and open to receiving feedback.

#### How To Contribute

1. Fork the repository: Start by forking this repository to your GitHub account. This will create a copy of the project
   under your account, allowing you to make changes without affecting the original codebase.

2. Clone the repository: Next, clone the repository to your local machine using the following command:

`git clone https://github.com/<your_username>/PyDocParser`

3. Create a new branch: Before making any changes, create a new branch to work on. Use a descriptive name that reflects
   the
   nature of your contribution. For example:

`git checkout -b new-feature-testing`

`git checkout -b bug-fix-123`

`git checkout -b documentation-update`

Also, if you're working on an issue, you can use the issue number as the branch name. For example:

`git checkout -b issue-123-bug`

`git checkout -b issue-456-docs`

`git checkout -b issue-789-feature`

4. Make your changes: Now, you can start making your desired changes to the project. Whether it's fixing a bug, adding a
   new feature, or improving the documentation, we appreciate all kinds of contributions.

5. Commit your changes: Once you're satisfied with your changes, commit them with a clear and concise commit message
   that
   describes the purpose of your modifications:

`git commit -m "Add my new feature"`

`git commit -m "Fix issue #123"`

`git commit -m "Update documentation (fixes #456)"`

6. Push your changes: Push your changes to your forked repository on GitHub.

`git push origin my-new-feature`

7. Open a pull request: Finally, open a pull request (PR) from your forked repository to the original repository.
   Provide a detailed description of the changes you've made, and I will review your contribution as soon as
   possible.

Thank you again for your interest and support in contributing to our project.

### License

This project is licensed under the MIT License, which is a permissive open-source license. It grants you the freedom to
use, modify, and distribute the software for any purpose. For more information, please refer to
the [LICENSE](LICENSE.md) file.

### Changelog

For a list of changes and new features, please refer to the [CHANGELOG](CHANGELOG.md) file.

### To-Do

This is just a small list of things that may be added in the future that I didn't want to create full issues for:

- [ ] Automate the generation of the documentation
- [ ] Automate the building and publishing of the package (both on PyPI and GitHub)

### Documentation

For more information, please refer to the [documentation](https://docparser.tautonico.tech/docs).

### Additional Information

This project is not affiliated with Docparser in any way. For more information about Docparser, please
  visit [their website](https://docparser.com/)

<br>

This project requires a minimum Python version of 3.8. It is designed to take advantage of the features and improvements introduced in Python 3.8 and later versions.

As of today (June 13, 2023), Python 3.7 is approaching its end-of-life (EOL) in only 14 days, on June 27, 2023. Python 2.x reached its EOL on January 1, 2020. It is strongly recommended to use a newer version of Python to ensure compatibility with the latest libraries and security patches.

Upgrading to a newer version of Python will provide you with access to the latest language features, performance enhancements, and bug fixes. It also ensures that you can take full advantage of the improvements in this project.

If you are currently using Python 2.x or Python 3.7, we encourage you to upgrade to Python 3.8 or a later version. The Python community provides comprehensive documentation and migration guides to assist you in the upgrade process.


<br>

This library has been recently updated. If you are using and older version, and need help migrating to the latest version,
please refer to the [migration guide](2.0.0->2023.06.a_migration_guide.md).