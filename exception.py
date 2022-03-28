from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def get_all_serializer_errors(e: ValidationError) -> dict:
    """This method manages the exception message returned in a more user friendly way to the frontend"""
    response_data = {}
    if type(e) is ValidationError:
        error = e.get_codes()
        if type(e.get_codes()) is dict:
            response_data = custom_error_message(e, error)
        return response_data
    return response_data


def custom_error_message(e, error):
    if len(e.args[0][''.join(list(error.keys())[0])]) > 1:
        message = e.args[0][''.join(list(error.keys())[0])][1]  # Default Serializer message or custom message
    else:
        message = e.args[0][''.join(list(error.keys())[0])][0]  # Default Serializer message or custom message
    error_code = list(error.values())[0]
    if len(error_code) > 1:
        str_error_code = ''.join(error_code[1])
    else:
        str_error_code = ''.join(error_code[0])
    field_name = list(error.keys())[0]
    if str_error_code == 'blank':
        error_code_switcher = {
            'blank': {'detail': _(f'Field {field_name} may not be blank'), 'status_code': 400},
        }
    elif str_error_code == 'required':
        error_code_switcher = {
            'required': {'detail': _(f'Field {field_name} is required'), 'status_code': 400},
        }
    elif str_error_code == 'max_length':
        error_code_switcher = {
            'max_length': {'detail': _(f'Ensure field {field_name} has no more than 6 characters.'), 'status_code': 400},
        }
    elif str_error_code == 'min_length':
        error_code_switcher = {
            'min_length': {'detail': _(f'Ensure field {field_name} has at least 6 characters.'), 'status_code': 400},
        }
    else:
        error_code_switcher = {
            'unique': {'detail': _(message), 'status_code': 400},
            'null': {'detail': _(message), 'status_code': 400},
            'invalid': {'detail': _(message), 'status_code': 400},
            'max_value': {'detail': _(message), 'status_code': 400},
            'min_value': {'detail': _(message), 'status_code': 400},
            'invalid_extension': {'detail': _(message), 'status_code': 400},
            'null_characters_not_allowed': {'detail': _(message), 'status_code': 400},
            'invalid_unicode': {'detail': _(message), 'status_code': 400},
            'max_string_length': {'detail': _(message), 'status_code': 400},
            'max_digits': {'detail': _(message), 'status_code': 400},
            'max_decimal_places': {'detail': _(message), 'status_code': 400},
            'max_whole_digits': {'detail': _(message), 'status_code': 400},
            'date': {'detail': _(message), 'status_code': 400},
            'make_aware': {'detail': _(message), 'status_code': 400},
            'overflow': {'detail': _(message), 'status_code': 400},
            'datetime': {'detail': _(message), 'status_code': 400},
            'invalid_choice': {'detail': _(message), 'status_code': 400},
            'empty': {'detail': _(message), 'status_code': 400},
            'no_name': {'detail': _(message), 'status_code': 400},
            'invalid_image': {'detail': _(message), 'status_code': 400},
            'not_a_dict': {'detail': _(message), 'status_code': 400},
            'not_a_list': {'detail': _(message), 'status_code': 400},
            'limit_value': {'detail': _(message), 'status_code': 400},
            'surrogate_characters_not_allowed': {'detail': _(message), 'status_code': 400}
        }
    return error_code_switcher.get(str_error_code, {})
