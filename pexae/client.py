# Copyright 2020 Pexeso Inc. All rights reserved.

from .lib import _lib, _AE_Client, _AE_MetadataSearch, _AE_AssetLibrary, \
    _AE_Status
from pexae.metadata_search import MetadataSearch
from pexae.asset_library import AssetLibrary
from pexae.errors import AEError


class Client(object):
    def __init__(self, client_id, client_secret):
        c_status = _AE_Status.new()
        c_client = _AE_Client.new()

        _lib.AE_Client_Init(c_client.get(), client_id.encode(),
                            client_secret.encode(), c_status.get())
        AEError.check_status(c_status)
        self._c_client = c_client

    def metadata_search(self):
        s = _AE_MetadataSearch.new(self._c_client.get())
        return MetadataSearch(s)

    def asset_library(self):
        l = _AE_AssetLibrary.new(self._c_client.get())
        return AssetLibrary(l)
