#!/usr/bin/env python3
"""Session authentication module for the API.
"""
from flask import request

from .auth import Auth


class SessionAuth(Auth):
    """Session authentication class.
    """
    pass
