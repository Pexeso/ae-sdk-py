# Copyright 2020 Pexeso Inc. All rights reserved.

from .lib import _lib, _AE_Client, _AE_MetadataSearch, _AE_AssetLibrary, \
    _AE_Status
from pexae.metadata_search import MetadataSearch
from pexae.asset_library import AssetLibrary
from pexae.errors import AEError


class Client(object):
    """ TODO """
    
    def __init__(self, client_id, client_secret):
        c_status = _AE_Status.new()
        c_client = _AE_Client.new()

        _lib.AE_Client_Init(c_client.get(), client_id.encode(),
                            client_secret.encode(), c_status.get())
        AEError.check_status(c_status)

        c_asset_library = _AE_AssetLibrary.new(c_client.get())
        c_metadata_search = _AE_MetadataSearch.new(c_client.get())

        self._c_client = c_client
        self._asset_library = AssetLibrary(c_asset_library)
        self._metadata_search = MetadataSearch(c_metadata_search)

    @property
    def asset_library(self):
        """
        An instance of the :class:`~pexae.AssetLibrary` class. All calls going
        through this instance will use the client's connection and
        authentication.
        """
        return self._asset_library

    @property
    def metadata_search(self):
        """
        An instance of the :class:`~pexae.MetadataSearch` class. All calls
        going through this instance will use the client's connection and
        authentication.
        """
        return self._metadata_search
