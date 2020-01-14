import base64
from json import loads

import requests

__author__ = "Steve Tautonico"
__contact__ = "stautonico@gmail.com"
__date__ = "7/11/19"
__version__ = 1.1


class Parser:
    """
    Python client for the docparser API
    """

    def __init__(self):
        """
        Constructor for the Parser class
        """
        # Note: This is required so any instances of `self.AUTH` don't error out if the user doesn't provide a key
        self.KEY = ""
        self.AUTH = (self.KEY, "")

    @staticmethod
    def check_request(request) -> bool:
        """
        Checks the status of a web request to check if any errors have occurred
        :param request: The result of the request
        :type request: requests.models.Response
        :return: True if no errors, otherwise false
        """
        if request.status_code == 403:
            print("Invalid API key. Use Parser.login(api_key)")
            return False
        elif requests.status_codes == 400:
            print("Error 400, bad request")
            return False
        else:
            return True

    def find_parser_id(self, parser) -> int:
        """
        Finds the id of the parser based on the name
        :param parser: The name of the parser
        :type parser: str
        :return: The id of the parser
        """
        parsers = self.parsers(True)
        for prsr in parsers:
            if parser in prsr["label"]:
                return prsr["id"]

    def login(self, key):
        """
        Initializes the `self.AUTH` with the user's API key
        :param key: The user's API key
        :type key: str
        :return: None
        """
        self.AUTH = (key, "")

    def ping(self) -> str:
        """
        Access the test `ping` page from the parser api
        :return: pong if the connection was successful
        """
        result = requests.get("https://api.docparser.com/v1/ping", auth=self.AUTH)
        success = self.check_request(result)
        if success:
            return loads(result.text)["msg"]

    def get_parsers(self, *verbose) -> dict or list:
        """
        Returns a list of all parsers available
        :param verbose: Enables verbose mode which returns raw json data (dict) from the request (with ids, label, etc)
        :type verbose: bool
        :return: A list of available parsers or the raw json data returned from the API
        """
        result = requests.get("https://api.docparser.com/v1/parsers", auth=self.AUTH)
        success = self.check_request(result)
        if success:
            if verbose:
                return loads(result.text)
            else:
                parsers = []
                for item in loads(result.text):
                    parsers.append(item["label"])
                return parsers

    def uploadbase64(self, file_base64, parser, filename) -> str or None:
        """
        Upload a file to docparser (already in base64 format)
        :param file_base64: The name of the file to upload
        :type file_base64: str
        :param parser: The name of the parser to send the file to
        :type parser: str
        :param filename: Filename of the file
        :type filename: str
        :return: The file id if the upload was successful, otherwise None
        """
        payload = {
            "file_content": file_base64,
            "file_name": filename
        }

        parser_id = self.find_parser_id(parser)
        result = requests.post("https://api.docparser.com/v1/document/upload/{}".format(parser_id),
                               auth=self.AUTH, data=payload)
        success = self.check_request(result)
        if success:
            result_loaded = loads(result.text)
            return result_loaded["id"]
        else:
            return None

    def upload(self, file, parser) -> str or None:
        """
        Upload a file to docparser
        :param file: The name of the file to upload
        :type file: str
        :param parser: The name of the parser to send the file to
        :type parser: str
        :return: The file id if the upload was successful, otherwise None
        """
        with open(file, "rb") as f:
            b64data = base64.b64encode(f.read())
        payload = {
            "file_content": b64data,
            "file_name": file
        }
        parser_id = self.find_parser_id(parser)
        result = requests.post("https://api.docparser.com/v1/document/upload/{}".format(parser_id),
                               auth=self.AUTH, data=payload)
        success = self.check_request(result)
        if success:
            result_loaded = loads(result.text)
            return result_loaded["id"]
        else:
            return None

    def upload_id(self, file, parser_id) -> str or None:
        """
        Upload a file to docparser
        :param file: The name of the file to upload
        :type file: str
        :param parser_id: The id of the parser to send the file to
        :type parser_id: str
        :return: The file id if the upload was successful, otherwise None
        """
        with open(file, "rb") as f:
            b64data = base64.b64encode(f.read())
        payload = {
            "file_content": b64data,
            "file_name": file
        }
        result = requests.post("https://api.docparser.com/v1/document/upload/{}".format(parser_id),
                               auth=self.AUTH, data=payload)
        success = self.check_request(result)
        if success:
            result_loaded = loads(result.text)
            return result_loaded["id"]
        else:
            return None

    def fetch(self, parser, doc_id) -> dict or None:
        """
        Retrieves the parsed data from a specific file (only one)
        :param parser: The name of the parser that was used to parse the file
        :type parser: str
        :param doc_id: ID of the doc to retrieve
        :type doc_id: str
        :return: The data parsed from the file if successful, otherwise None
        """
        parser_id = self.find_parser_id(parser)
        result = requests.get("https://api.docparser.com/v1/results/{}/{}".format(parser_id, doc_id), auth=self.AUTH)
        success = self.check_request(result)
        if success:
            try:
                return loads(result.text)[0]
            except KeyError:
                print("No such document exists")
                return None
        else:
            return None

    def fetch_id(self, parser_id, doc_id) -> dict or None:
        """
        Retrieves the parsed data from a specific file (only one)
        :param parser_id: The id of the parser that was used to parse the file
        :type parser_id: str
        :param doc_id: ID of the doc to retrieve
        :type doc_id: str
        :return: The data parsed from the file if successful, otherwise None
        """
        result = requests.get("https://api.docparser.com/v1/results/{}/{}".format(parser_id, doc_id), auth=self.AUTH)
        success = self.check_request(result)
        if success:
            try:
                return loads(result.text)[0]
            except KeyError:
                print("No such document exists")
                return None
        else:
            return None

    def fetch_all(self, parser) -> list or None:
        """
        Retrieves all the parsed data currently in a parser
        :param parser: The name of the parser to retrieve that data from
        :type parser: str
        :return: A list of all the data from the parser if there is data, otherwise none
        """
        parser_id = self.find_parser_id(parser)
        result = requests.get("https://api.docparser.com/v1/results/{}".format(parser_id), auth=self.AUTH)
        success = self.check_request(result)
        if success:
            return loads(result.text)
        else:
            return None

    def fetch_all_id(self, parser_id) -> list or None:
        """
        Retrieves all the parsed data currently in a parser
        :param parser_id: The id of the parser to retrieve that data from
        :type parser_id: str
        :return: A list of all the data from the parser if there is data, otherwise none
        """
        result = requests.get("https://api.docparser.com/v1/results/{}".format(parser_id), auth=self.AUTH)
        success = self.check_request(result)
        if success:
            return loads(result.text)
        else:
            return None
