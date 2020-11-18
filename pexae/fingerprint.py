# Copyright 2020 Pexeso Inc. All rights reserved.

import ctypes

from pexae.lib import _lib, _AE_Status, _AE_Buffer, _AE_Fingerprint
from pexae.errors import AEError

    
class Fingerprint(object):
    @staticmethod
    def from_file(path):
        status = _AE_Status.new()
        ft = _AE_Fingerprint.new()

        _lib.AE_Fingerprint_FromFile(ft.get(), path.encode(), status.get())
        AEError.check_status(status)
        return Fingerprint(ft)

    @staticmethod
    def from_buffer(data):
        status = _AE_Status.new()
        ft = _AE_Fingerprint.new()
        buf = _AE_Buffer.new()

        _lib.AE_Buffer_Set(buf.get(), data, len(data))

        _lib.AE_Fingerprint_FromBuffer(ft.get(), buf.get(), status.get())
        AEError.check_status(status)
        return Fingerprint(ft)

    @staticmethod
    def load(data):
        ft = _AE_Fingerprint.new()
        buf = _AE_Buffer.new()

        _lib.AE_Buffer_Set(buf.get(), data, len(data))
        _lib.AE_Fingerprint_Load(ft.get(), buf.get())
        return Fingerprint(ft)

    def __init__(self, ft):
        self._ft = ft

    def dump(self):
        buf = _AE_Buffer.new()

        _lib.AE_Fingerprint_Dump(self._ft.get(), buf.get())
        data = _lib.AE_Buffer_GetData(buf.get())
        size = _lib.AE_Buffer_GetSize(buf.get())
        return ctypes.string_at(data, size)
