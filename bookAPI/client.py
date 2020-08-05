from json import JSONDecodeError

import requests
from rest_framework import status
from rest_framework.exceptions import ValidationError


class Client:
    def __init__(self, path):
        self.path = path

    def get_books(self, query):
        try:
            return requests.get(
                self.path + '?q={}'.format(query)).json()
        except JSONDecodeError:
            raise ValidationError("Cannot parse google books api!", code=status.HTTP_400_BAD_REQUEST)
