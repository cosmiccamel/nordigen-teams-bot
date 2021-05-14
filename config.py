#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "8cf6656d-0338-4a5a-9ae0-b73d6c881a4f")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "9GjNks4YvJ_JtQL-__aRiqe2vP03696Q_z")
