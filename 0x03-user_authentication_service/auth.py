#!/usr/bin/env python3
''' Hash password '''
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    ''' a function that hashes password'''
    salt = bcrypt.gensalt()
    passWord = password

    hashed_password = bcrypt.hashpw(passWord.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    ''' generates uuid and returns a string representation'''
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ a function that registers users
        """
        user = self._db.find_user_by(email=email)
        hashed_password = _hash_password(password)
        if user:
            raise ValueError(f'User {email} already exists')
        return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """ Credentials validation """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                user_pw = user.hashed_password
                input_password = password.encode("utf-8")
                return bcrypt.checkpw(input_password, user_pw)
        except (NoResultFound, InvalidRequestError):
            return False
        return False
