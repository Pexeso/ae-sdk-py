# Copyright 2020 Pexeso Inc. All rights reserved.

import ctypes
from datetime import datetime
from collections import namedtuple
from enum import Enum

from pexae.lib import _lib, _AE_Status, _AE_Fingerprint, \
    _AE_MetadataSearchRequest, _AE_MetadataSearchResult, \
    _AE_MetadataSearchMatch, _AE_MetadataSearchFuture
from pexae.errors import AEError
from pexae.common import Segment
from pexae.asset_library import AssetType


class MetadataSearchRequest(object):
    """
    Holds all data necessary to perform a metadata search. Currently, a search
    can only be performed using a fingerprint, but more parameters can be
    supported in the future.
    """

    def __init__(self, fingerprint):
        self._fingerprint = fingerprint

    @property
    def fingerprint(self):
        """
        A fingerprint generated from a file or a byte buffer.

        :type: Fingerprint
        """
        return self._fingerprint

    def __repr__(self):
        return "MetadataSearchRequest(fingerprint=...)"


class MetadataSearchMatch(object):
    """
    Contains detailed information about the match, including information about
    the matched asset, and the matching segments.
    """

    def __init__(self, asset_id, asset_type, segments):
        self._asset_id = asset_id
        self._asset_type = asset_type
        self._segments = segments

    @property
    def asset_id(self):
        """
        An ID that uniquely identifies a matching asset. This can be used to
        retrieve detailed information about the asset using
        :meth:`AssetLibrary.get_asset`.

        :type: int
        """
        return self._asset_id

    @property
    def asset_type(self):
        """
        One of: recording, composition, video.

        :type: AssetType
        """
        return self._asset_type

    @property
    def segments(self):
        """
        A list of matching :class:`Segment` instances.

        :type: list
        """
        return self._segments

    def __repr__(self):
        return "MetadataSearchMatch(asset_id={},asset_type={},segments={})".format(
                self.asset_id, self.asset_type, self.segments)


class MetadataSearchResult(object):
    """
    This object is returned from :meth:`MetadataSearchFuture.get` upon
    successful comptetion.
    """

    def __init__(self, lookup_id, matches):
        self._lookup_id = lookup_id
        self._matches = matches

    @property
    def lookup_id(self):
        """
        An ID that uniquely identifies a particular search. Can be used for
        diagnostics.

        :type: int
        """
        return self._lookup_id

    @property
    def matches(self):
        """
        A list of :class:`MetadataSearchMatch`.

        :type: list
        """
        return self._matches

    def __repr__(self):
        return "MetadataSearchResult(lookup_id={},matches=<{} objects>)".format(
                self.lookup_id, len(self.matches))


class MetadataSearchFuture(object):
    """
    This object is returned by the :meth:`MetadataSearch.start` method
    and is used to retrieve a search result.
    """

    def __init__(self, c_fut):
        self._c_fut = c_fut

    def get(self):
        """
        Blocks until the search result is ready and then returns it.

        :raise: :class:`AEError` if the search couldn't be performed, e.g.
                because of network issues.
        :rtype: MetadataSearchResult
        """

        c_status = _AE_Status.new(_lib)
        c_res = _AE_MetadataSearchResult.new(_lib)

        _lib.AE_MetadataSearchFuture_Get(self._c_fut.get(), c_res.get(),
                                         c_status.get())
        AEError.check_status(c_status)

        c_match = _AE_MetadataSearchMatch.new(_lib)
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
            matches=matches)


class MetadataSearch(object):
    """
    This class encapsulates all operations necessary to perform a metadata
    search. Instead of instantiating the class directly,
    :attr:`Client.metadata_search` should be used.
    """

    def __init__(self, c_search):
        self._c_search = c_search

    def start(self, req):
        """
        Starts a metadata search. This operation does not block until the
        search is finished, it does however perform a network operation to
        initiate the search on the backend service.

        :param MetadataSearchRequest req: search parameters.
        :raise: :class:`AEError` if the search couldn’t be initiated, e.g.
                because of network issues.
        :rtype: MetadataSearchFuture
        """
        c_status = _AE_Status.new(_lib)
        c_req = _AE_MetadataSearchRequest.new(_lib)
        c_fut = _AE_MetadataSearchFuture.new(_lib)

        _lib.AE_MetadataSearchRequest_SetFingerprint(
            c_req.get(), req.fingerprint._c_ft.get())

        _lib.AE_MetadataSearch_Start(self._c_search.get(), c_req.get(),
                                  c_fut.get(), c_status.get())
        AEError.check_status(c_status)
        return MetadataSearchFuture(c_fut)


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
