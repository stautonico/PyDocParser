__author__ = "Steve Tautonico"
__contact__ = "stautonico@gmail.com"
__date__ = "2023-06-12T00:00:00"
__version__ = "2023.06.a"

from datetime import datetime
import os

from typing import Optional, Union, List, Dict, Literal

import requests


class Docparser:
    """
    A class wrapper for the docparser API.
    This class covers all the API endpoints available from https://docparser.com/api
    """

    def __init__(self):
        self._BASE_URL = "https://api.docparser.com/v1"
        self._api_key = None

    def login(self, api_key: str) -> bool:
        """
        Login to the docparser API.
        Args:
            api_key (str): The API key to use for authentication.

        Returns:
            bool: True if login was successful, False otherwise.
        """
        self._api_key = api_key

        return self.ping()

    def _make_authenticated_request(self, method: str, url: str, data: dict = None,
                                    files: dict = None) -> requests.Response:
        """
        Make an authenticated request to the docparser API.
        Args:
            method (str): The HTTP method to use.
            url (str): The URL to make the request to.
            data (dict): The data to send with the request.
            files (dict): The files to send with the request.

        Returns:
            requests.Response: The response object.
        """
        return requests.request(method, url, data=data, files=files, auth=(self._api_key, ""))

    def ping(self) -> bool:
        """
        Ping the docparser API to test the connection.
        (wrapper for https://api.docparser.com/v1/ping)
        Returns:
            bool: True if the connection was successful, False otherwise.
        """
        url = self._BASE_URL + "/ping"
        response = self._make_authenticated_request("GET", url)
        if response.status_code == 200:
            # Just confirm that our response looks like "{"msg": "pong"}"
            return response.json().get("msg") == "pong"
        else:
            return False

    def _get_parser_id_by_label(self, parser_label: str) -> Optional[str]:
        """
        Get the parser ID by the parser label.
        Args:
            parser_label (str): The parser label to search for.

        Returns:
            Optional[str]: The parser ID if found, None otherwise.
        """
        try:
            parsers = self.list_parsers()
        except Exception as e:
            raise e

        for parser in parsers:
            if parser.get("label") == parser_label:
                return parser.get("id")

        return None

    def _check_parser_id_exists(self, parser_label: str) -> Optional[str]:
        """
        Check if the parser ID exists.
        Args:
            parser_label (str): The parser label to search for.

        Returns:
            Optional[str]: The parser ID if found, None otherwise.
        """
        try:
            parser_id = self._get_parser_id_by_label(parser_label)
        except Exception as e:
            raise e

        if parser_id is None:
            raise Exception(f"Parser label \"{parser_label}\" not found.")

        return parser_id

    # Parser Routes
    def list_parsers(self) -> Union[List[dict], str]:
        """
        Get a list of all document parsers linked to the current account.
        (wrapper for https://api.docparser.com/v1/parsers)

        Returns:
            Optional[Union[List[dict], str]]: A list of all document parsers linked to the current account, or an exception if the request failed including the error message.
        """
        result = self._make_authenticated_request("GET", self._BASE_URL + "/parsers")

        if result.status_code == 200:
            if type(result.json()) == list:
                return result.json()

        raise Exception(result.text)

    def list_parser_model_layouts(self, parser_label: str) -> Union[List[dict], str]:
        """
        Get a list of all the Model Layouts for a specific parser by label.
        (wrapper for https://api.docparser.com/v1/parser/models/<PARSER_ID>)
        Args:
            parser_label (str): The parser label to search for.

        Returns:
            Optional[Union[List[dict], str]]: A list of all the Model Layouts for a specific parser by label, or an exception if the request failed including the error message.
        """
        parser_id = self._check_parser_id_exists(parser_label)

        result = self._make_authenticated_request("GET", self._BASE_URL + "/parser/models/" + parser_id)

        if result.status_code == 200:
            if type(result.json()) == list:
                return result.json()

        raise Exception(result.text)

    # Document Routes
    def upload_local_file_by_path(self, path: str, parser_label: str, remote_id: Optional[str] = None) -> str:
        """
        Upload a local file (by file path) to a specific parser (by label)
        (wrapper for https://api.docparser.com/v1/document/upload/<PARSER_ID>)
        Args:
            path (str): The file path to upload.
            parser_label (str): The parser label to upload to.
            remote_id (str): The ID of the remote file being uploaded. (optional)

        Returns:
            Optional[str]: The document ID if successful, raises an exception otherwise.
        """
        parser_id = self._check_parser_id_exists(parser_label)

        path = os.path.expanduser(path)

        # Check if the file exists
        if not os.path.exists(path):
            raise Exception(f"File path {path} does not exist.")

        files = {"file": open(path, "rb")}
        result = self._make_authenticated_request("POST", self._BASE_URL + "/document/upload/" + parser_id,
                                                  data={"remote_id": remote_id}, files=files)

        if result.status_code == 200:
            return result.json().get("id")

        raise Exception(result.text)

    def upload_file_by_base64(self, base64_file_content: bytes, filename: str, parser_label: str,
                              remote_id: Optional[str] = None) -> str:
        """
        Upload a file by base64 encoded content to a specific parser (by label)
        (wrapper for https://api.docparser.com/v1/document/upload/<PARSER_ID>)
        Args:
            base64_file_content (bytes): The base64 encoded file content.
            filename (str): The filename of the file being uploaded.
            parser_label (str): The parser label to upload to.
            remote_id (str): The ID of the remote file being uploaded. (optional)

        Returns:
            Optional[str]: The document ID if successful, raises an exception otherwise.
        """
        parser_id = self._check_parser_id_exists(parser_label)

        payload = {
            "file_content": base64_file_content,
            "file_name": filename,
            "remote_id": remote_id
        }

        result = self._make_authenticated_request("POST", self._BASE_URL + "/document/upload/" + parser_id,
                                                  data=payload)

        if result.status_code == 200:
            return result.json().get("id")

        raise Exception(result.text)

    def upload_file_by_url(self, url: str, parser_label: str, remote_id: Optional[str] = None) -> str:
        """
        Upload a file (by public URL) to a specific parser (by label)
        (wrapper for https://api.docparser.com/v1/document/fetch/<PARSER_ID>)
        Args:
            url (str): The public URL of the file to upload.
            parser_label (str): The parser label to upload to.
            remote_id (str): The ID of the remote file being uploaded. (optional)

        Returns:
            Optional[str]: The document ID if successful, raises an exception otherwise.
        """
        parser_id = self._check_parser_id_exists(parser_label)

        payload = {
            "url": url,
            "remote_id": remote_id
        }

        result = self._make_authenticated_request("POST", self._BASE_URL + "/document/fetch/" + parser_id,
                                                  data=payload)

        if result.status_code == 200:
            return result.json().get("id")

        raise Exception(result.text)

    def get_one_result(self, parser_label: str, document_id: str, include_children: Optional[bool] = False) -> List[
        Dict[str, Union[str, int]]]:
        """
        Get the parsed result of a single document by ID.
        (wrapper for https://api.docparser.com/v1/results/<PARSER_ID>/<DOCUMENT_ID>)
        Note that the "format" option is currently not supported.
        Args:
            parser_label (str): The parser label to search for.
            document_id (str): The document ID to search for.
            include_children (bool): Whether to include the children of the result. (optional)
                                     Examples include documents created while splitting documents, etc.
        Returns:
            Optional[List[Dict[str, Union[str, int]]]]: The parsed result of a single document by ID, raises an exception otherwise.
        """
        parser_id = self._check_parser_id_exists(parser_label)

        payload = {
            "include_children": include_children,
        }

        result = self._make_authenticated_request("POST", self._BASE_URL + "/results/" + parser_id + "/" + document_id,
                                                  data=payload)

        if result.status_code == 200:
            return result.json()

        raise Exception(result.text)

    def get_multiple_results(self, parser_label: str,
                             _list: Literal["last_uploaded", "uploaded_after", "processed_after"] = "last_uploaded",
                             limit: int = 100, date: datetime = None, remote_id: Optional[str] = None,
                             include_processing_queue: bool = False, sort_by: Literal[
                "parsed_at", "processed_at", "uploaded_at", "first_processed_at", "imported_at", "integrated_at", "dispatched_webook_at", "preprocessed_at"] = "uploaded_at",
                             sort_order: Literal["asc", "desc"] = "desc") -> List[Dict[str, Union[str, int]]]:
        """
        Get multiple results from a parser by label.
        (wrapper for https://api.docparser.com/v1/results/<PARSER_ID>
        Note: The "format" option is currently not supported.
        Args:
            parser_label (str): The parser label to search for.
            _list (Literal["last_uploaded", "uploaded_after", "processed_after"]): The type of documents to list. (optional)
            limit (int): The maximum number of results to return (if list is == "last_uploaded".) (optional)
            date (datetime): Used for "uploaded_after" and "processed_after" (optional, mandatory if _list is "uploaded_after" or "processed_after")
            remote_id (str): The remote ID to search for. (optional)
            include_processing_queue (bool): Whether to include files that are still processing (optional)
            sort_by (Literal["parsed_at", "processed_at", "uploaded_at", "first_processed_at", "imported_at", "integrated_at", "dispatched_webook_at", "preprocessed_at"]): The field to sort by. (optional)
            sort_order (Literal["asc", "desc"]): The sort order. (optional)
        """
        parser_id = self._check_parser_id_exists(parser_label)

        if _list == "uploaded_after" or _list == "processed_after":
            if date is None:
                raise Exception("date must be provided if _list is 'uploaded_after' or 'processed_after'")

            date = date.isoformat()

        payload = {
            "list": _list,
            "limit": limit,
            "date": date,
            "remote_id": remote_id,
            "include_processing_queue": include_processing_queue,
            "sort_by": sort_by,
            "sort_order": sort_order.upper()
        }

        result = self._make_authenticated_request("POST", self._BASE_URL + "/results/" + parser_id, data=payload)

        if result.status_code == 200:
            return result.json()

        raise Exception(result.text)
