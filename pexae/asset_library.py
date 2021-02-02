# Copyright 2020 Pexeso Inc. All rights reserved.

import ctypes
from collections import namedtuple
from enum import Enum

from pexae.lib import _lib, _AE_Status,  _AE_Asset, _AE_AssetMetadata, \
        _AE_AssetLicensors
from pexae.errors import AEError


class AssetType(Enum):
    """
    Searches performed through the SDK match against 'assets' representing
    copywritten works. Assets are categorized as Recording, Composition, or
    Video Asset Types.

    A single piece of content may match against all three asset types. E.g, a
    music video uploaded could match to a Video Asset controlled by a record
    label, a Recording Asset controlled by the same label, and a Composition
    Asset controlled by a CMO representing the song writer.
    """

    RECORDING = 0
    """
    An audio recording. Searched content may match a recording asset via 1-1
    audio matches, or by matching it's melody (e.g a cover song)
    """

    COMPOSITION = 1
    """
    The composition representing the underlying lyrics and melody of a song.
    Composition Assets are linked to associated Recording Assets.
    """

    VIDEO = 2
    """
    A copywritten audio-visual work.
    """


class AssetMetadata(object):
    """
    Metadata associated with an asset. Usually it comes as part of the
    :class:`Asset` class which can be retrieved using the
    :meth:`AssetLibrary.get_asset` method.
    """

    def __init__(self, isrc, title, artists, upcs, licensors):
        self._isrc = isrc
        self._title = title
        self._artists = artists
        self._upcs = upcs
        self._licensors = licensors

    @property
    def isrc(self):
        """
        An international standard code for uniquely identifying sound
        recordings and music video recordings.
        """
        return self._isrc

    @property
    def title(self):
        """
        The name of the track recording for a given ISRC.
        """
        return self._title

    @property
    def artists(self):
        """
        The names of the recording artists for a given ISRC.
        """
        return self._artists

    @property
    def upcs(self):
        """
        The unique codes associated with the sale of a recording.
        """
        return self._upcs

    @property
    def licensors(self):
        """
        The entities that own the rights to the given UPC and are entitled to
        license its use and collect royalties.

        It is a dictionary where the key is a territory code that conforms to
        the ISO 3166-1 alpha-2 standard. For more information visit
        https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2.
        """
        return self._licensors

    def __repr__(self):
        return "AssetMetadata(isrc={},title={},artists={},upcs={},licensors={})".format(
                self.isrc, self.title, self.artists, self.upcs, self.licensors)


class Asset(object):
    """
    This class represents an asset and the data associated with it. You can use
    :meth:`AssetLibrary.get_asset` to retrieve an asset.
    """

    def __init__(self, metadata):
        self._metadata = metadata

    @property
    def metadata(self):
        """
        The metadata associated with an asset. See :class:`~AssetMetadata` for
        more information.
        """
        return self._metadata

    def __repr__(self):
        return "Asset(metadata=...)"


class AssetLibrary(object):
    """
    This class encapsulates all operations on assets. Instead of
    instantiating the class directly, :attr:`Client.asset_library`
    should be used.
    """

    def __init__(self, library):
        self._c_library = library

    def get_asset(self, asset_id):
        """
        Retrieve information about an asset based on an asset ID.

        :param int asset_id: ID of the asset whose information we're trying to retrieve.
        :raise: :class:`AEError` if the asset cannot be retrieved.
        :return: An asset.
        :rtype: Asset
        """

        c_status = _AE_Status.new(_lib)
        c_asset = _AE_Asset.new(_lib)

        _lib.AE_AssetLibrary_GetAsset(self._c_library.get(), asset_id,
                                      c_asset.get(), c_status.get())
        AEError.check_status(c_status)

        c_metadata = _AE_AssetMetadata.new(_lib)
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
    c_asset_licensors = _AE_AssetLicensors.new(_lib)
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
