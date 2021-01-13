# Copyright 2020 Pexeso Inc. All rights reserved.

import ctypes
from datetime import datetime
from collections import namedtuple
from enum import Enum

from pexae.lib import _lib, _AE_Status, _AE_Fingerprint, \
    _AE_LicenseSearchRequest, _AE_LicenseSearchResult, _AE_LicenseSearchFuture
from pexae.errors import AEError
from pexae.common import Segment
from pexae.asset_library import AssetType


class BasicPolicy(Enum):
    """ TODO """

    ALLOW = 0
    BLOCK = 1


class LicenseSearchResult(object):
    """ TODO """
    def __init__(self, lookup_id, completed_at, policies):
        self._lookup_id = lookup_id
        self._completed_at = completed_at
        self._policies = policies

    @property
    def lookup_id(self):
        """ TODO """
        return self._lookup_id

    @property
    def completed_at(self):
        """ TODO """
        return self._completed_at

    @property
    def policies(self):
        """ TODO """
        return self._policies

    def __repr__(self):
        return "LicenseSearchResult(lookup_id={},completed_at={},policies={})".format(
                self.lookup_id, self.completed_at, self.policies)


class LicenseSearchRequest(object):
    """ TODO """

    def __init__(self, fingerprint):
        self._fingerprint = fingerprint

    @property
    def fingerprint(self):
        """ TODO """
        return self._fingerprint

    def __repr__(self):
        return "LicenseSearchRequest(fingerprint=...)"


class LicenseSearchFuture(object):
    def __init__(self, c_fut):
        self._c_fut = c_fut


    def get(self):
        c_status = _AE_Status.new(_lib)
        c_res = _AE_LicenseSearchResult.new(_lib)

        _lib.AE_LicenseSearchFuture_Get(self._c_fut.get(), c_res.get(),
                                        c_status.get())
        AEError.check_status(c_status)

        policies = {}
        c_territory = ctypes.c_char_p()
        c_policy = ctypes.c_int()
        c_policies_pos = ctypes.c_size_t(0)

        while _lib.AE_LicenseSearchResult_NextPolicy(
                c_res.get(),
                ctypes.byref(c_territory),
                ctypes.byref(c_policy),
                ctypes.byref(c_policies_pos)):
            policies[c_territory.value.decode()] = BasicPolicy(c_policy.value)

        completed_at = datetime.fromtimestamp(
            _lib.AE_LicenseSearchResult_GetCompletedAt(c_res.get()))

        return LicenseSearchResult(
            lookup_id=_lib.AE_LicenseSearchResult_GetLookupID(c_res.get()),
            completed_at=completed_at,
            policies=policies)


class LicenseSearch(object):
    """ TODO """

    def __init__(self, c_search):
        self._c_search = c_search

    def start(self, req):
        """ TODO """
        c_status = _AE_Status.new(_lib)
        c_req = _AE_LicenseSearchRequest.new(_lib)
        c_fut = _AE_LicenseSearchFuture.new(_lib)

        _lib.AE_LicenseSearchRequest_SetFingerprint(
            c_req.get(), req.fingerprint._c_ft.get())

        _lib.AE_LicenseSearch_Start(self._c_search.get(), c_req.get(),
                                    c_fut.get(), c_status.get())
        AEError.check_status(c_status)
        return LicenseSearchFuture(c_fut)
