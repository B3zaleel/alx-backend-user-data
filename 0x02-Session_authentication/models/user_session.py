#!/usr/bin/env python3
"""User session module.
"""
from models.base import Base


class UserSession(Base):
    """User session class.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """Initializes a User session instance.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
