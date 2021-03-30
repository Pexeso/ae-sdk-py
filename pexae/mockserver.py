# Copyright 2020 Pexeso Inc. All rights reserved.

from .lib import _lib, _AE_Client, _AE_Status
from pexae.client import Client
from pexae.errors import AEError


class Mockserver(object):
    """
    This class encapsulates operations required for communicating with the mockserver.
    """

    @staticmethod
    def new_client(client_id, client_secret):
        """
        Creates a new instance of the client using provided credentials
        for authentication.

        :param string client_id: this can be found in the official mockserver documentation.
        :param string client_secret: this can be found in the official mockserver documentation.
        :raise: :class:`AEError` if the connection cannot be established
                or the provided authentication credentials are invalid.
        """

        c_status = _AE_Status.new(_lib)
        c_client = _AE_Client.new(_lib)

        _lib.AE_Mockserver_InitClient(c_client.get(), client_id.encode(),
                                      client_secret.encode(), c_status.get())
        AEError.check_status(c_status)
        return Client(c_client)
