from datetime import datetime
from json import loads

import requests

__author__ = "Steve Tautonico"
__contact__ = "stautonico@gmail.com"
__date__ = "7/7/2022"
__version__ = 2.1

try:
    from typing import Literal
except:
    from typing_extensions import Literal
from typing import Optional, Union, List


class Parser:
    """
    Python client for docparser API
    """

    def __init__(self):
        """
        Constructor for the Parser class
        """
        self.BASE_URL = "https://api.docparser.com/v1"
        self.KEY = ""
        self.AUTH = (self.KEY, "")
        self.PARSER_DICT = {}

    def login(self, key: str) -> None:
        """
        Initializes the `self.AUTH` with the user's API key

        :param key: The user's API key
        :type key: str
        :return: None
        """
        self.AUTH = (key, "")
        assert self.ping() == "pong"
        self._populate_parser_dict(self.list_parsers())

    def ping(self) -> Optional[str]:
        """
        Try to send an authenticated ping to the docparser API

        :return: 'pong' if the connection was successful, else None
        """
        result = requests.get(self.BASE_URL + "/ping", auth=self.AUTH)

        success, message = self._check_request(result)

        if success:
            return loads(result.text)["msg"]

        return message

    def list_parsers(self) -> Optional[Union[List[dict], str]]:
        """
        Get a list of all document parsers linked to the given API key

        :return: A list of dicts containing the parser's id and label if successful, None if failure
        """
        result = requests.get(self.BASE_URL + "/parsers", auth=self.AUTH)

        success, message = self._check_request(result)

        if success:
            return loads(result.text)

        return message

    def list_parser_model_layouts(self, parser_label=None) -> Union[str, list]:
        """
         List all of the model layouts for a specific parser linked to the given API key

        :param parser_label: The label of the parser to find
        :return: String error message or list of parser model layouts
        """
        parser_id = self._find_parser_id(parser_label)

        if not parser_id:
            return "Unable to find parser"

        result = requests.get(self.BASE_URL + "/parser/models/" + parser_id, auth=self.AUTH)

        success = self._check_request(result)

        if success:
            return loads(result.text)

        return "Failed to get parser model layouts"

    def upload_file_by_path(self, file_path: str, parser_label: str, remote_id: str) -> str:
        """
        Try to upload a file to the given parser label using a local file path.
        The http processor (requests) handles sending the file to the server

        :param file_path: The full file path of the file on the local file system
        :param parser_label: The label of the parser to upload the file to
        :param remote_id: Association id for after the document has been parsed
        :return: An error message or the id of the uploaded document
        """
        try:
            file = open(file_path, "rb")
        except FileNotFoundError:
            return "Failed to read file"

        # Check that the parser exists
        parser_id = self._find_parser_id(parser_label)

        if not parser_id:
            return "Unable to find parser"

        payload = {
            "remote_id": remote_id
        }

        result = requests.post(
            self.BASE_URL + "/document/upload/" + parser_id,
            auth=self.AUTH,
            files={"file": file},
            data=payload
        )

        success, message = self._check_request(result)

        if success:
            result_loaded = loads(result.text)
            return result_loaded["id"]

        return message

    def upload_file_by_base64(self, file_content: bytes, filename: str, parser_label: str, remote_id: str) -> str:
        """
        Try to upload a file to the given parser label using the raw base64 content

        :param file_content: The base64 content of the file to upload
        :param filename: The name of the file being uploaded
        :param parser_label: The label of the parser to upload the file to
        :param remote_id: Association id for after the document has been parsed
        :return: An error message or the id of the uploaded document
        """
        parser_id = self._find_parser_id(parser_label)

        if not parser_id:
            return "Unable to find parser"

        payload = {
            "file_content": file_content,
            "file_name": filename,
            "remote_id": remote_id
        }

        result = requests.post(self.BASE_URL + "/document/upload/" + parser_id, auth=self.AUTH, data=payload)

        success, message = self._check_request(result)

        if success:
            result_loaded = loads(result.text)
            return result_loaded["id"]

        return message

    def upload_file_by_url(self, file_url: str, parser_label: str, remote_id: str) -> str:
        """
        Try to upload a file to the given parser label by fetching a file from an external url

        :param file_url: The url of the file to fetch and send to docparser
        :param parser_label: The label of the parser to upload the file to
        :param remote_id: Association id for after the document has been parsed
        :return: An error message or the id of the uploaded document
        """
        parser_id = self._find_parser_id(parser_label)

        if not parser_id:
            return "Unable to find parser"

        payload = {
            "url": file_url,
            "remote_id": remote_id
        }

        result = requests.post(self.BASE_URL + "/document/fetch/" + parser_id, auth=self.AUTH, data=payload)

        success, message = self._check_request(result)

        if success:
            result_loaded = loads(result.text)
            return result_loaded["id"]

        return message

    def get_one_result(self, parser_label: str, document_id: str, include_children: Optional[boolean]=False) -> Union[str, dict]:
        """
        Get a specific document result from the given parser by document_id

        :param parser_label: The label of the parser to retrieve the document result from
        :param document_id: The id of the document to receive
        :return: A string error message or a dict containing the document result
        """
        parser_id = self._find_parser_id(parser_label)

        if not parser_id:
            return "Unable to find parser"

        if include_children:
            result = requests.get(self.BASE_URL + "/results/{}/{}/?include_children=true/".format(parser_id, document_id), auth=self.AUTH)
        else:
            result = requests.get(self.BASE_URL + "/results/{}/{}".format(parser_id, document_id), auth=self.AUTH)

        # This needs its own error checking because status 400 isn't always a bad thing
        if result.status_code == 403:
            return "Invalid API key, use Parser.login(api_key)"
        else:
            return loads(result.text)

    def get_multiple_results(self, parser_label: str, format: Literal["object", "flat"] = "object",
                             list: Literal["last_uploaded", "uploaded_after", " processed_after"] = "last_uploaded",
                             limit: int = 100, date: Optional[datetime] = None, remote_id: Optional[str] = None,
                             include_processing_queue: Optional[bool] = None) -> Union[str, dict]:
        """
        Get multiple document results based on the given set of rules from the docparser API docs:
        https://dev.docparser.com/?shell#get-data-of-one-document

        :param parser_label: The label of the parser to retrieve the document result from
        :param format:
        :param list:
        :param limit:
        :param date:
        :param remote_id:
        :param include_processing_queue:
        :return: A string error message or a dict containing the document result
        """
        parser_id = self._find_parser_id(parser_label)

        if not parser_id:
            return "Unable to find parser"

        payload = {
            format: format,
            list: list,
            limit: limit
        }

        if date:
            payload["date"] = date.isoformat()

        if remote_id:
            payload["remote_id"] = remote_id

        if include_processing_queue:
            payload["include_processing_queue"] = include_processing_queue

        result = requests.get(self.BASE_URL + "/results/" + parser_id, auth=self.AUTH, data=payload)

        # This needs its own error checking because status 400 isn't always a bad thing
        if result.status_code == 403:
            return "Invalid API key, use Parser.login(api_key)"
        else:
            return loads(result.text)

    # Internal functions #

    def _populate_parser_dict(self, parsers: list[dict]):
        for parser in parsers:
            self.PARSER_DICT[parser["label"]] = parser["id"]

    def _find_parser_id(self, parser_label) -> Optional[str]:
        """
        Finds the id of the parser based on the label

        :param parser_label: The name of the parser
        :type parser_label: str
        :return: The id of the parser
        """
        parser_id = self.PARSER_DICT[parser_label]

        if not parser_id:
            self._populate_parser_dict(self.list_parsers())
            return self.PARSER_DICT[parser_label]
        else:
            return parser_id

    @staticmethod
    def _check_request(request) -> (bool, str):
        """
        Checks the status of a request to see if any errors have occurred.
        Used to prevent having to manually check each status code on each endpoint

        :param request: The result of the request
        :type request: requests.models.Response
        :return: `True` and an empty string if successful, `False` and an error message if failure
        """
        if request.status_code == 403:
            return False, "Invalid API key, use Parser.login(<YOUR API KEY>)"
        elif request.status_code == 400:
            return False, "Error 400, bad request"
        else:
            return True, ""
