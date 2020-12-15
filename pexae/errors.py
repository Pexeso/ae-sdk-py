# Copyright 2020 Pexeso Inc. All rights reserved.

from enum import Enum

from pexae.lib import _lib


class Code(Enum):
    OK = 0
    DEADLINE_EXCEEDED = 1
    PERMISSION_DENIED = 2
    UNAUTHENTICATED = 3
    NOT_FOUND = 4
    NOT_UNIQUE = 5
    INVALID_INPUT = 6
    OUT_OF_MEMORY = 7
    INTERNAL_ERROR = 8


class AEError(RuntimeError):
    """
    TODO
    """

    @staticmethod
    def check_status(c_status):
        if not _lib.AE_Status_OK(c_status.get()):
            raise AEError.from_status(c_status)
        
    @staticmethod
    def from_status(c_status):
        code = _lib.AE_Status_GetCode(c_status.get())
        message = _lib.AE_Status_GetMessage(c_status.get())
        return AEError(Code(code), message.decode())

    def __init__(self, code, message):
        super().__init__("{}: {}".format(code, message))
        self._code = Code(code)
        self._message = message

    @property
    def code(self):
        """ TODO """
        return self._code

    @property
    def message(self):
        """ TODO """
        return self._message
