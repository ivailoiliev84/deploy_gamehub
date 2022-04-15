from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


def validator_only_letters_numbers(value):
    for letter in value:
        if not letter.isalpha() and not letter.isdigit() and letter != '_':
            raise ValidationError('Ensure this value contains only letters, numbers, and underscore.')


@deconstructible
class ValidatorMaxSizeInMB:
    def __init__(self, max_size):
        self.max_size = max_size

    def __call__(self, value):
        file_size = value.file.size
        if file_size > self.__convert_megabytes_to_bytes(self.max_size):
            raise ValidationError(self.__exception_message())

    def __convert_megabytes_to_bytes(self, value):
        return value * 1024 * 1024

    def __exception_message(self):
        return f"Max file size is {self.max_size:.f2}MB"
