# -*- coding: utf-8 -*-
from starlette import status

# from apps.users.api_errors import UsersApiErrors
# from config.openapi import ApiError
from config.utils.exceptions import AuthEmailException


def generate_nested_schema_for_code(responses, error_code):
    responses[error_code] = {}
    responses[error_code]["content"] = {}
    responses[error_code]["content"]["application/json"] = {}


def error_responses(*args: AuthEmailException, auth=False) -> dict:
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
            "value": {
                "detail": [
                    {
                        "code": "validation-error",
                        "type": "string",
                        "message": "string",
                        "location": "(body, query, path, header)",
                        "field": "string",
                    },
                ],
            },
        },
    }
    responses[status.HTTP_422_UNPROCESSABLE_ENTITY]["content"]["application/json"]["examples"] = example
