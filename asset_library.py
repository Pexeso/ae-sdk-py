#!/usr/bin/env python3
# Copyright 2020 Pexeso Inc. All rights reserved.

import ctypes
from collections import namedtuple
from enum import Enum

from .lib import _lib, _AE_Status,  _AE_Asset, _AE_AssetMetadata, \
        _AE_AssetLicensors
from .errors import AEError


class AssetType(Enum):
    RECORDING = 0
    COMPOSITION = 1
    VIDEO = 2
    IMAGE = 3
    TEXT = 4


class AssetLicensors(object):
    def __init__(self, asset_id, asset_type, segments):
        self._asset_id = asset_id
        self._asset_type = asset_type
        self._segments = segments

    @property
    def asset_id(self):
        return self._asset_id

    @property
    def asset_type(self):
        return self._asset_type

    @property
    def segments(self):
        return self._segments


class AssetMetadata(object):
    def __init__(self, lookup_id, completed_at, matches):
        self._lookup_id = lookup_id
        self._completed_at = completed_at
        self._matches = matches
    
    @property
    def lookup_id(self):
        return self._lookup_id

    @property
    def completed_at(self):
        return self._completed_at

    @property
    def lookup_id(self):
        return self._lookup_id


class Asset(object):
    def __init__(self):
        pass


class AssetLibrary(object):
    def __init__(self, client):
        self._library = library

    def get_asset(self, kwargs, asset_id):
        c_status = _AE_Status.new()
        c_asset = _AE_Asset.new()

        _lib.AE_AssetLibrary_GetAsset(self._library.get(), asset_id,
                                      c_asset.get(), c_status.get())
        AEError.check_status(c_status)

        c_metadata = _AE_AssetMetadata.new()
        _lib.AE_Asset_GetMetadata(c_asset.get(), c_metadata.get())

        return Asset(metadata=AssetMetadata(
            isrc=_AE_AssetMetadata_GetISRC(c_metadata.get()).decode(),
            title=_AE_AssetMetadata_GetTitle(c_metadata.get()).decode(),
            artists=artists,
            upcs=upcs,
            licensors=licensors,
        ))
