#!/usr/bin/env python3
# Copyright 2020 Pexeso Inc. All rights reserved.

import ctypes
from collections import namedtuple
from enum import Enum

from .lib import _lib, _AE_Status, _AE_Fingerprint, \
    _AE_MetadataSearchRequest, _AE_MetadataSearchResult, \
    _AE_MetadataSearchMatch
from .errors import AEError
from .common import Segment
from .asset_library import AssetType


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


class MetadataSearchRequest(object):
    def __init__(self, fingerprint):
        self._fingerprint = fingerprint

    @property
    def fingerprint(self):
        return self._fingerprint


class MetadataSearch(object):
    def __init__(self, c_search):
        self._c_search = c_search

    def do(self, req):
        c_status = _AE_Status.new()
        c_req = _AE_MetadataSearchRequest.new()
        c_res = _AE_MetadataSearchResult.new()

        _lib.AE_MetadataSearchRequest_SetFingerprint(
            c_req.get(), req.fingerprint._ft.get())

        _lib.AE_MetadataSearch_Do(self._c_search.get(), c_req.get(),
                                  c_res.get(), c_status.get())
        AEError.check_status(c_status)

        # extract the result
        c_match = _AE_MetadataSearchMatch.new()
        c_matches_pos = ctypes.c_size_t(0)

        matches = []
        while _lib.AE_MetadataSearchResult_NextMatch(
                c_res.get(), c_match.get(), ctypes.byref(c_matches_pos)):
            matches.append(MetadataSearchMatch(
                asset_id=_lib.AE_MetadataSearchMatch_GetAssetID(c_match.get()),
                asset_type=AssetType(_lib.AE_MetadataSearchMatch_GetAssetType(c_match.get())),
                segments=_extract_metadata_search_segments(c_match)))

        return MetadataSearchResult(
            lookup_id=_lib.AE_MetadataSearchResult_GetLookupID(c_res.get()),
            completed_at=_lib.AE_MetadataSearchResult_GetCompletedAt(c_res.get()), # TODO: convert to datetime
            matches=matches)


def _extract_metadata_search_segments(c_match):
    c_query_start = ctypes.c_int64(0)
    c_query_end = ctypes.c_int64(0)
    c_asset_start = ctypes.c_int64(0)
    c_asset_end = ctypes.c_int64(0)
    c_segments_pos = ctypes.c_size_t(0)

    segments = []
    while _lib.AE_MetadataSearchMatch_NextSegment(
            c_match.get(), ctypes.byref(c_query_start), ctypes.byref(c_query_end),
            ctypes.byref(c_asset_start), ctypes.byref(c_asset_end),
            ctypes.byref(c_segments_pos)):
        segments.append(Segment(
            query_start=c_query_start.value,
            query_end=c_query_end.value,
            asset_start=c_asset_start.value,
            asset_end=c_asset_end.value))
    return segments
