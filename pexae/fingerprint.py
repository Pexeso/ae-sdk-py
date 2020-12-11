# Copyright 2020 Pexeso Inc. All rights reserved.

import ctypes

from pexae.lib import _lib, _AE_Status, _AE_Buffer, _AE_Fingerprint
from pexae.errors import AEError

    
class Fingerprint(object):
    """
    Fingerprint is how the SDK identifies a piece of digital content.  It can
    be generated from a media file or from a memory buffer. The content must be
    encoded in one of the supported formats and must be longer than 1 second.
    """

    @staticmethod
    def from_file(path):
        """
        Generate a fingerprint from a file stored on a disk. The parameter to
        the function must be a path to a valid file in supported format.
        """
        status = _AE_Status.new()
        ft = _AE_Fingerprint.new()

        _lib.AE_Fingerprint_FromFile(ft.get(), path.encode(), status.get())
        AEError.check_status(status)
        return Fingerprint(ft)

    @staticmethod
    def from_buffer(data):
        """
        Generate a fingerprint from a media file loaded in memory as a byte
        buffer.
        """
        status = _AE_Status.new()
        ft = _AE_Fingerprint.new()
        buf = _AE_Buffer.new()

        _lib.AE_Buffer_Set(buf.get(), data, len(data))

        _lib.AE_Fingerprint_FromBuffer(ft.get(), buf.get(), status.get())
        AEError.check_status(status)
        return Fingerprint(ft)

    @staticmethod
    def load(data):
        """
        Load a fingerprint previously serialized by the Fingerprint.Dump()
        function.
        """
        ft = _AE_Fingerprint.new()
        buf = _AE_Buffer.new()

        _lib.AE_Buffer_Set(buf.get(), data, len(data))
        _lib.AE_Fingerprint_Load(ft.get(), buf.get())
        return Fingerprint(ft)

    def __init__(self, ft):
        self._ft = ft

    def dump(self):
        """
        Serialize the fingerprint into a byte slice so that it can be stored on
        a disk or in a dabase. It can later be deserialized with the load()
        function.
        """
        buf = _AE_Buffer.new()

        _lib.AE_Fingerprint_Dump(self._ft.get(), buf.get())
        data = _lib.AE_Buffer_GetData(buf.get())
        size = _lib.AE_Buffer_GetSize(buf.get())
        return ctypes.string_at(data, size)
