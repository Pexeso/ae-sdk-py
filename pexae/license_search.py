# Copyright 2020 Pexeso Inc. All rights reserved.

import ctypes
from datetime import datetime
from collections import namedtuple
from enum import Enum

from pexae.lib import _lib, _AE_Status, _AE_Fingerprint, \
    _AE_LicenseSearchRequest, _AE_LicenseSearchResult
from pexae.errors import AEError
from pexae.common import Segment
from pexae.asset_library import AssetType


class LicenseSearchResult(object):
    """ TODO """
    def __init__(self, lookup_id, completed_at, restricted_countries):
        self._lookup_id = lookup_id
        self._completed_at = completed_at
        self._restricted_countries = restricted_countries

    @property
    def lookup_id(self):
        """ TODO """
        return self._lookup_id

    @property
    def completed_at(self):
        """ TODO """
        return self._completed_at

    @property
    def restricted_countries(self):
        """ TODO """
        return self._restricted_countries

    def __repr__(self):
        return "LicenseSearchResult(lookup_id={},completed_at={},restricted_countries={})".format(
                self.lookup_id, self.completed_at, self.restricted_countries)


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


class LicenseSearch(object):
    """ TODO """
    
    def __init__(self, c_search):
        self._c_search = c_search

    def do(self, req):
        """ TODO """
        c_status = _AE_Status.new()
        c_req = _AE_LicenseSearchRequest.new()
        c_res = _AE_LicenseSearchResult.new()

        _lib.AE_LicenseSearchRequest_SetFingerprint(
            c_req.get(), req.fingerprint._c_ft.get())

        _lib.AE_LicenseSearch_Do(self._c_search.get(), c_req.get(),
                                  c_res.get(), c_status.get())
        AEError.check_status(c_status)

        restricted_countries = []
        c_restricted_country = ctypes.c_char_p()
        c_restricted_countries_pos = ctypes.c_size_t(0)

        while _lib.AE_LicenseSearchResult_NextRestrictedTerritory(
                c_res.get(),
                ctypes.byref(c_restricted_country),
                ctypes.byref(c_restricted_countries_pos)):
            restricted_countries.append(c_restricted_country.value.decode())

        completed_at = datetime.fromtimestamp(
            _lib.AE_LicenseSearchResult_GetCompletedAt(c_res.get()))

        return LicenseSearchResult(
            lookup_id=_lib.AE_LicenseSearchResult_GetLookupID(c_res.get()),
            completed_at=completed_at,
            restricted_countries=set(restricted_countries))
