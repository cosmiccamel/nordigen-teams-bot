# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
#
# from botbuilder.schema import Attachment


class UserProfile:
    """
      This is our application state. Just a regular serializable Python class.
    """

    def __init__(self, name: str = None, country: str = None, bank_id: str = None,
                 bank_title:str= None):
        self.name = name
        self.country = country
        self.bank_id = bank_id
        self.bank_title = bank_title
