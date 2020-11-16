#!/usr/bin/env python3
# Copyright 2020 Pexeso Inc. All rights reserved.

class Client(object):
    def __init__(self, client_id, client_secret):
        self._client = _AE_Client.new(client_id, client_secret)

    def metadata_search(self):
        s = _AE_MetadataSearch.new(self._client.get())
        return MetadataSearch(s)

    def asset_library(self):
        l = _AE_AssetLibrary.new(self._client.get())
        return AssetLibrary(l)