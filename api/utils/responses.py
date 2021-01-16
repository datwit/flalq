#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import make_response, jsonify

SUCCESS_200 = {'http_code': 200, 'code': 'success', 'message': 'Showed'}

SUCCESS_201 = {'http_code': 201, 'code': 'success', 'message': 'The request was fulfilled and a new resource has been created'}

SUCCESS_204 = {'http_code': 204, 'code': 'success', 'message': '204 204 no Content '}


BAD_REQUEST_400 = {"http_code": 400, "code": "bad Request", "message": "The server can’t process the request due to a client error"}

UNAUTHORIZED_401 = {"http_code": 401, "code": "not Authorized", "message": "Invalid authentication"}

FORBIDDEN_403 = {"http_code": 403, "code": "no tAuthorized", "message": "The requesting client is not authorized to obtain the resource"}

SERVER_ERROR_404 = {"http_code": 404, "code": "not Found", "message": "The requested resource doesn’t exist on the server"}

NOT_FOUND_HANDLER_404 = {"http_code": 404, "code": "not Found", "message": "Route not found"}

INVALID_FIELD_NAME_SENT_422 = {"http_code": 422, "code": "invalid Field", "message": "Invalid fields found"}

INVALID_INPUT_422 = {"http_code": 422, "code": "invalid Input", "message": "The request can’t be processed due to semantic error"}

MISSING_PARAMETERS_422 = {"http_code": 422, "code": "missing Parameter", "message": "Missing parameters."}

SERVER_ERROR_500 = {"http_code": 500, "code": "server Error", "message": "Generic error to imply an unexpected condition in server"}


def response_with(response, value=None, message=None, error=None, headers={}, pagination=None):
    result = {}
    if value is not None:
        result.update(value)

    if response.get('message', None) is not None:
        result.update({'Message': response['message']})

    result.update({'code': response['code']})

    if error is not None:
        result.update({'errors': error})

    if pagination is not None:
        result.update({'pagination': pagination})

    headers.update({'Access-Control-Allow-Origin': '*'})
    headers.update({'server': 'Flask REST API'})

    return make_response(jsonify(result), response['http_code'], headers)
