# -*- coding: utf-8 -*-
import re

from email_validator import EmailNotValidError, validate_email


async def validate_email_(email):
    data = {}
    try:
        validation = validate_email(email, check_deliverability=True)
        data["email"] = validation.email
    except EmailNotValidError as e:
        data["message"] = str(e)
    return data


async def validate_password(password):
    return True if re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{8,20}$", password) else False


async def validate_username(username):
    if re.match(r"^[\w\d +]{5,40}$", username) and len([letter for letter in username if letter.isalpha()]) >= 4:
        return True
    return False
