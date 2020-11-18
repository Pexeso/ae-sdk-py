# Copyright 2020 Pexeso Inc. All rights reserved.

import ctypes
from collections import namedtuple
from enum import Enum

from pexae.lib import _lib, _AE_Status,  _AE_Asset, _AE_AssetMetadata, \
        _AE_AssetLicensors
from pexae.errors import AEError


class AssetType(Enum):
    RECORDING = 0
    COMPOSITION = 1
    VIDEO = 2
    IMAGE = 3
    TEXT = 4


class AssetMetadata(object):
    def __init__(self, isrc, title, artists, upcs, licensors):
        self._isrc = isrc
        self._title = title
        self._artists = artists
        self._upcs = upcs
        self._licensors = licensors
    
    @property
    def isrc(self):
        return self._isrc

    @property
    def title(self):
        return self._title

    @property
    def artists(self):
        return self._artists

    @property
    def upcs(self):
        return self._upcs

    @property
    def licensors(self):
        return self._licensors

    def __repr__(self):
        return "AssetMetadata(isrc={},title={},artists={},upcs={},licensors={})".format(
                self.isrc, self.title, self.artists, self.upcs, self.licensors)

class Asset(object):
    def __init__(self, metadata):
        self._metadata = metadata

    @property
    def metadata(self):
        return self._metadata

    def __repr__(self):
        return "Asset(metadata=...)"

class AssetLibrary(object):
    def __init__(self, library):
        self._c_library = library

    def get_asset(self, asset_id):
        c_status = _AE_Status.new()
        c_asset = _AE_Asset.new()

        _lib.AE_AssetLibrary_GetAsset(self._c_library.get(), asset_id,
                                      c_asset.get(), c_status.get())
        AEError.check_status(c_status)

        c_metadata = _AE_AssetMetadata.new()
        _lib.AE_Asset_GetMetadata(c_asset.get(), c_metadata.get())

        return Asset(metadata=AssetMetadata(
            isrc=_lib.AE_AssetMetadata_GetISRC(c_metadata.get()).decode(),
            title=_lib.AE_AssetMetadata_GetTitle(c_metadata.get()).decode(),
            artists=_extract_artists(c_metadata),
            upcs=_extract_upcs(c_metadata),
            licensors=_extract_licensors(c_metadata),
        ))


def _extract_artists(c_metadata):
    artists = []
    c_artist = ctypes.c_char_p()
    c_artists_pos = ctypes.c_size_t(0)
    while _lib.AE_AssetMetadata_NextArtist(c_metadata.get(),
                                           ctypes.byref(c_artist),
                                           ctypes.byref(c_artists_pos)):
        artists.append(c_artist.value.decode())
    return artists


def _extract_upcs(c_metadata):
    upcs = []
    c_upc = ctypes.c_char_p()
    c_upcs_pos = ctypes.c_size_t(0)
    while _lib.AE_AssetMetadata_NextUPC(c_metadata.get(),
                                        ctypes.byref(c_upc),
                                        ctypes.byref(c_upcs_pos)):
        upcs.append(c_upc.value.decode())
    return upcs


def _extract_licensors(c_metadata):
    asset_licensors = {}
    c_asset_licensors = _AE_AssetLicensors.new()
    c_asset_licensors_pos = ctypes.c_size_t(0)
    while _lib.AE_AssetMetadata_NextLicensors(
            c_metadata.get(), c_asset_licensors.get(),
            ctypes.byref(c_asset_licensors_pos)):
        licensors = []
        c_licensor = ctypes.c_char_p()
        c_licensors_pos = ctypes.c_size_t(0)
        while _lib.AE_AssetLicensors_NextLicensor(
                c_asset_licensors.get(), ctypes.byref(c_licensor),
                ctypes.byref(c_licensors_pos)):
            licensors.append(c_licensor.value.decode())

        territory = _lib.AE_AssetLicensors_GetTerritory(
            c_asset_licensors.get()).decode()
        asset_licensors[territory] = licensors
    return asset_licensors
