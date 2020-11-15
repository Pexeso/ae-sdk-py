#!/usr/bin/env python3
# Copyright 2020 Pexeso Inc. All rights reserved.

from enum import Enum

from .lib import _lib


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
    @staticmethod
    def check_status(status):
        if not _lib.AE_Status_OK(status.get()):
            raise AEError.from_status(status)
        
    @staticmethod
    def from_status(status):
        code = _lib.AE_Status_GetCode(status.get())
        message = _lib.AE_Status_GetMessage(status.get())
        return AEError(Code(code), message.decode())

    def __init__(self, code, message):
        super().__init__("{}: {}".format(code, message))
        self.code = Code(code)
        self.message = message
