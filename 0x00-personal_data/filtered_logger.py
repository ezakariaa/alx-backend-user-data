#!/usr/bin/env python3
"""
Module for handling Personal Data
"""
from typing import List
import re
import logging
import os
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Returns the log message obfuscated

    Args:
        fields (List[str]): a list of strings representing all fields.
        redaction (str): a string representing by what the field.
        message (str): a string representing the log line
        separator (str): a string representing by which character is separating
                         all fields in the log line

    Returns:
        str: The obfuscated log message
    """
    for field in fields:
        message = re.sub(f'{field}=[^{separator}]*', f'{field}={redaction}',
                         message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class

    This class redacts sensitive information from log messages.
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize the formatter

        Args:
            fields (List[str]): list of fields to redact
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record

        Args:
            record (logging.LogRecord): the log record

        Returns:
            str: the formatted and redacted log message
        """
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, message,
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Returns a Logger object

    Returns:
        logging.Logger: Configured logger
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to a MySQL database

    Returns:
        mysql.connector.connection.MySQLConnection: database connection
    """
    db_connect = mysql.connector.connect(
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.getenv("PERSONAL_DATA_DB_NAME"),
    )
    return db_connect


def main():
    """
    Obtain a database connection using get_db and retrieve all rows
    in the users table, displaying each row in a filtered format
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()

    for row in cursor:
        message = "; ".join([f"{key}={value}" for key, value in row.items()])
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
