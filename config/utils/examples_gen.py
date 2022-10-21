# -*- coding: utf-8 -*-
from fastapi_helper import DefaultHTTPException
from starlette import status

# from apps.users.api_errors import UsersApiErrors
# from config.openapi import ApiError


def generate_nested_schema_for_code(responses, error_code):
    responses[error_code] = {}
    responses[error_code]["content"] = {}
    responses[error_code]["content"]["application/json"] = {}


def error_responses(*args: DefaultHTTPException, auth: bool = False) -> dict:
    # TODO: fix (try classes)
    # TODO: exceptions for (401, 403)

    error_codes = {error.status_code for error in args}
    responses = {}

    for error_code in error_codes:
        examples = {}

        for error in args:
            if error.status_code == error_code:
                examples[error.type] = error.example()

        generate_nested_schema_for_code(responses, error_code)
        responses[error_code]["content"]["application/json"]["examples"] = examples

    # if auth:
    #     generate_nested_schema_for_code(responses, status.HTTP_403_FORBIDDEN)
    #     example = {UsersApiErrors.NOT_AUTHORIZED.type: UsersApiErrors.NOT_AUTHORIZED.example()}
    #     responses[status.HTTP_403_FORBIDDEN]["content"]["application/json"]["examples"] = example
    #     generate_nested_schema_for_code(responses, status.HTTP_401_UNAUTHORIZED)
    #     example = {UsersApiErrors.LOGIN_REQUIRED.type: UsersApiErrors.LOGIN_REQUIRED.example()}
    #     example2 = {UsersApiErrors.INVALID_CREDENTIALS.type: UsersApiErrors.INVALID_CREDENTIALS.example()}
    #     responses[status.HTTP_401_UNAUTHORIZED]["content"]["application/json"]["examples"] = {
    #         **example,
    #         **example2,
    #     }
    change_422_validation_schema(responses)

    return responses


def change_422_validation_schema(responses):
    generate_nested_schema_for_code(responses, status.HTTP_422_UNPROCESSABLE_ENTITY)
    example = {
        "validation_errors": {
            "summary": "Validation Error",
            "value": [
                {
                    "code": "validation-error",
                    "type": "string",
                    "message": "string",
                    "field": "string",
                },
            ],
        },
    }
    responses[status.HTTP_422_UNPROCESSABLE_ENTITY]["content"]["application/json"]["examples"] = example
