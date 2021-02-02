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
    """
    An enumeration of possible license policies for queried content.
    """

    ALLOW = 0
    """
    The content should be allowed to be uploaded to the platform.
    """

    BLOCK = 1
    """
    The content should not be allowed to be uploaded to the platform, because
    it includes copyrighted content.
    """


class LicenseSearchRequest(object):
    """
    Holds all data necessary to perform a license search. Currently, a search
    can only be performed using a fingerprint, but more parameters can be
    supported in the future.
    """

    def __init__(self, fingerprint):
        self._fingerprint = fingerprint

    @property
    def fingerprint(self):
        """
        An fingerprint generated from a file or a byte buffer.

        :type: Fingerprint
        """
        return self._fingerprint

    def __repr__(self):
        return "LicenseSearchRequest(fingerprint=...)"


class LicenseSearchResult(object):
    """
    This object is returned from :meth:`LicenseSearchFuture.get` upon
    successful comptetion.
    """

    def __init__(self, lookup_id, policies):
        self._lookup_id = lookup_id
        self._policies = policies

    @property
    def lookup_id(self):
        """
        An ID that uniquely identifies a particular search. Can be used for
        diagnostics.

        :type: int
        """
        return self._lookup_id

    @property
    def policies(self):
        """
        A dict where the key is a territory and the value is an instance of
        :class:`BasicPolicy`. The territory codes conform to
        the ISO 3166-1 alpha-2 standard. For more information visit
        https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2.

        :type: dict
        """
        return self._policies

    def __repr__(self):
        return "LicenseSearchResult(lookup_id={},policies={})".format(
                self.lookup_id, self.policies)


class LicenseSearchFuture(object):
    """
    This object is returned by the :meth:`LicenseSearch.start` method
    and is used to retrieve a search result.
    """

    def __init__(self, c_fut):
        self._c_fut = c_fut

    def get(self):
        """
        Blocks until the search result is ready and then returns it.

        :raise: :class:`AEError` if the search couldn't be performed, e.g.
                because of network issues.
        :rtype: LicenseSearchResult
        """

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

        return LicenseSearchResult(
            lookup_id=_lib.AE_LicenseSearchResult_GetLookupID(c_res.get()),
            policies=policies)


class LicenseSearch(object):
    """
    This class encapsulates all operations necessary to perform a license
    search. Instead of instantiating the class directly,
    :attr:`Client.license_search` should be used.
    """

    def __init__(self, c_search):
        self._c_search = c_search

    def start(self, req):
        """
        Starts a license search. This operation does not block until the
        search is finished, it does however perform a network operation to
        initiate the search on the backend service.

        :param LicenseSearchRequest req: search parameters.
        :raise: :class:`AEError` if the search couldn’t be initiated, e.g.
                because of network issues.
        :rtype: LicenseSearchFuture
        """

        c_status = _AE_Status.new(_lib)
        c_req = _AE_LicenseSearchRequest.new(_lib)
        c_fut = _AE_LicenseSearchFuture.new(_lib)

        _lib.AE_LicenseSearchRequest_SetFingerprint(
            c_req.get(), req.fingerprint._c_ft.get())

        _lib.AE_LicenseSearch_Start(self._c_search.get(), c_req.get(),
                                    c_fut.get(), c_status.get())
        AEError.check_status(c_status)
        return LicenseSearchFuture(c_fut)
