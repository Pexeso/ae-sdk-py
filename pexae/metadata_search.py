# Copyright 2020 Pexeso Inc. All rights reserved.

import ctypes
from datetime import datetime
from collections import namedtuple
from enum import Enum

from pexae.lib import _lib, _AE_Status, _AE_Fingerprint, \
    _AE_MetadataSearchRequest, _AE_MetadataSearchResult, \
    _AE_MetadataSearchMatch
from pexae.errors import AEError
from pexae.common import Segment
from pexae.asset_library import AssetType


class MetadataSearchMatch(object):
    """ TODO """
    
    def __init__(self, asset_id, asset_type, segments):
        self._asset_id = asset_id
        self._asset_type = asset_type
        self._segments = segments

    @property
    def asset_id(self):
        """ TODO """
        return self._asset_id

    @property
    def asset_type(self):
        """ TODO """
        return self._asset_type

    @property
    def segments(self):
        """ TODO """
        return self._segments

    def __repr__(self):
        return "MetadataSearchMatch(asset_id={},asset_type={},segments={})".format(
                self.asset_id, self.asset_type, self.segments)


class MetadataSearchResult(object):
    """ TODO """
    def __init__(self, lookup_id, completed_at, matches):
        self._lookup_id = lookup_id
        self._completed_at = completed_at
        self._matches = matches

    @property
    def lookup_id(self):
        """ TODO """
        return self._lookup_id

    @property
    def completed_at(self):
        """ TODO """
        return self._completed_at

    @property
    def matches(self):
        """ TODO """
        return self._matches

    def __repr__(self):
        return "MetadataSearchResult(lookup_id={},completed_at={},matches=...)".format(
                self.lookup_id, self.completed_at)


class MetadataSearchRequest(object):
    """ TODO """
    
    def __init__(self, fingerprint):
        self._fingerprint = fingerprint

    @property
    def fingerprint(self):
        """ TODO """
        return self._fingerprint

    def __repr__(self):
        return "MetadataSearchRequest(fingerprint=...)"


class MetadataSearch(object):
    """ TODO """
    
    def __init__(self, c_search):
        self._c_search = c_search

    def do(self, req):
        """ TODO """
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

        completed_at = datetime.fromtimestamp(
            _lib.AE_MetadataSearchResult_GetCompletedAt(c_res.get()))

        return MetadataSearchResult(
            lookup_id=_lib.AE_MetadataSearchResult_GetLookupID(c_res.get()),
            completed_at=completed_at,
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
