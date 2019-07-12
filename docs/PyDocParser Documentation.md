## PyDocParser Documentation



## Classes

**pydocparser.Parser**

The main parser class from the module. This class contains all the functions to interact with the docparser API.

## Internal Functions

Parser.**check_request(*request*)**

Internal function that handles most error checking. The request argument is the output of a given http request. The function checks the status code of the request to see if an error has occurred. If an error has occurred, the function will return false and and error code.

Parser.**find_parser_id(*parser*)**

Internal function that, given the parsers name, returns its id number. This function is used so users can just enter the name of the parser without having to try to find its id.

## Functions

Parser.**login(*key*)**

Using the users **API KEY** (*key*), this function returns an auth object that is passed to the API for user authentication.

Parser.**ping()**

A test function provided by the docparser API. Calling this function will return *“pong”* if connection to the API was successful, and *None* if the connection was unsuccessful.

Parser.**get_parsers(&ast;*verbose*)**

Calling this functions returns a list of all available parsers on the user’s account. If you want the ID’s of the parsers, you can set `verbose` to `True` to get a raw output from the request (JSON data including the parser ID + label)

Parser.**upload(*file*, *parser*)**

This function is used to upload a file to docparser. The `file` argument is the filename to open and send to the parser. (Note: the file must be accessible to the python script that is being executed.) The `parser` argument is the name of the parser to send the data to. After uploading, the function returns the document ID number.

Parser.**upload_id(*file*, *parser_id*)**

This function is used to upload a file to docparser. The `file` argument is the filename to open and send to the parser. (Note: the file must be accessible to the python script that is being executed.) The `parser_id` argument is the id of the parser to send the data to. After uploading, the function returns the document ID number.

Parser.**fetch(*parser*, *doc_id*)**

This function is used to retrieve parsed data from a specific file. The `parser` argument is the name of the parser to retrieve data from. The `doc_id` argument is the ID number of the document to receive parsed data from.

Parser.**fetch_id(*parser_id*, *doc_id*)**

This function is used to retrieve parsed data from a specific file. The `parser` argument is the name of the parser to retrieve data from. The `doc_id` argument is the ID number of the document to receive parsed data from.

Parser.**fetch_all((*parser*)**

Retrieves all parsed data that is currently stored within a parser. The `parser` argument is the name of the parser to retrieve data from.

Parser.**fetch_all_id((*parser_id*)**

Retrieves all parsed data that is currently stored within a parser. The `parser_id` argument is the ID  of the parser to retrieve data from.

