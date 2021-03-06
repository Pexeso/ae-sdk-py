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

        :param str path: path to the media file we're trying to fingerprint.
        :raise: :class:`AEError` if the media file is missing or invalid.
        :rtype: Fingerprint
        """

        c_status = _AE_Status.new(_lib)
        c_ft = _AE_Fingerprint.new(_lib)

        _lib.AE_Fingerprint_FromFile(c_ft.get(), path.encode(), c_status.get())
        AEError.check_status(c_status)
        return Fingerprint(c_ft)

    @staticmethod
    def from_buffer(buf):
        """
        Generate a fingerprint from a media file loaded in memory as a byte
        buffer.

        :param bytes buf: A byte buffer holding a media file.
        :raise: :class:`AEError` if the buffer holds invalid data.
        :rtype: Fingerprint
        """

        c_status = _AE_Status.new(_lib)
        c_ft = _AE_Fingerprint.new(_lib)
        c_buf = _AE_Buffer.new(_lib)

        _lib.AE_Buffer_Set(c_buf.get(), buf, len(buf))

        _lib.AE_Fingerprint_FromBuffer(c_ft.get(), c_buf.get(), c_status.get())
        AEError.check_status(c_status)
        return Fingerprint(c_ft)

    @staticmethod
    def load(buf):
        """
        Load a fingerprint previously serialized by the :meth:`~dump` function.

        :param bytes buf: A byte buffer holding serialized fingerprint.
        :raise: :class:`AEError` if the data inside buf is invalid.
        :rtype: Fingerprint
        """

        c_ft = _AE_Fingerprint.new(_lib)
        c_buf = _AE_Buffer.new(_lib)

        _lib.AE_Buffer_Set(c_buf.get(), buf, len(buf))
        _lib.AE_Fingerprint_Load(c_ft.get(), c_buf.get())
        return Fingerprint(c_ft)

    def __init__(self, c_ft):
        self._c_ft = c_ft

    def dump(self):
        """
        Serialize the fingerprint into a byte slice so that it can be stored on
        a disk or in a database. It can later be deserialized with the
        :meth:`~load` function.

        :return: A byte buffer with serialized fingerprint.
        :rtype: bytes
        """
        c_buf = _AE_Buffer.new(_lib)

        _lib.AE_Fingerprint_Dump(self._c_ft.get(), c_buf.get())
        data = _lib.AE_Buffer_GetData(c_buf.get())
        size = _lib.AE_Buffer_GetSize(c_buf.get())
        return ctypes.string_at(data, size)
