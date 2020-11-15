#!/usr/bin/env python3
# Copyright 2020 Pexeso Inc. All rights reserved.

import ctypes
from collections import namedtuple
from enum import Enum

from .lib import _lib, _AE_Status, _AE_Fingerprint, \
    _AE_MetadataSearchRequest, _AE_MetadataSearchResult,
    _AE_MetadataSearchMatch
from .errors import AEError


class MetadataSearchMatch(object):
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


class MetadataSearchResult(object):
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


class MetadataSearch(object):
    def __init__(self, client):
        self._search = search

    def do(self, req):
        pass ## TODO: implement
