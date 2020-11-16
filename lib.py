#!/usr/bin/env python3
# Copyright 2020 Pexeso Inc. All rights reserved.

import ctypes
import ctypes.util
import platform


class _SafeObject(object):
    def __init__(self, new, delete, args=[]):
        self._obj = new(*args)
        if not self._obj:
            raise MemoryError("out of memory")
        self._delete = delete

    def __del__(self):
        self._delete(ctypes.byref(self._obj))

    def get(self):
        return self._obj


class _AE_Status(ctypes.Structure):
    @staticmethod
    def new():
        return _SafeObject(_lib.AE_Status_New, _lib.AE_Status_Delete)


class _AE_Buffer(ctypes.Structure):
    @staticmethod
    def new():
        return _SafeObject(_lib.AE_Buffer_New, _lib.AE_Buffer_Delete)


class _AE_Fingerprint(ctypes.Structure):
    @staticmethod
    def new():
        return _SafeObject(_lib.AE_Fingerprint_New, _lib.AE_Fingerprint_Delete)


class _AE_Client(ctypes.Structure):
    @staticmethod
    def new():
        return _SafeObject(
            _lib.AE_Client_New,
            _lib.AE_Client_Delete,
            args=[client_id.encode(), client_secret.encode()])


class _AE_MetadataSearch(ctypes.Structure):
    @staticmethod
    def new(client):
        return _SafeObject(
            _lib.AE_MetadataSearch_New,
            _lib.AE_MetadataSearch_Delete,
            args=[client])


class _AE_MetadataSearchRequest(ctypes.Structure):
    @staticmethod
    def new(client):
        return _SafeObject(
            _lib.AE_MetadataSearchRequest_New,
            _lib.AE_MetadataSearchRequest_Delete)


class _AE_MetadataSearchResult(ctypes.Structure):
    @staticmethod
    def new(client):
        return _SafeObject(
            _lib.AE_MetadataSearchResult_New,
            _lib.AE_MetadataSearchResult_Delete)


class _AE_MetadataSearchMatch(ctypes.Structure):
    @staticmethod
    def new(client):
        return _SafeObject(
            _lib.AE_MetadataSearchMatch_New,
            _lib.AE_MetadataSearchMatch_Delete)


class _AE_AssetLibrary(ctypes.Structure):
    @staticmethod
    def new(client):
        return _SafeObject(
            _lib.AE_AssetLibrary_New,
            _lib.AE_AssetLibrary_Delete,
            args=[client])


class _AE_AssetMetadata(ctypes.Structure):
    @staticmethod
    def new(client):
        return _SafeObject(
            _lib.AE_AssetMetadata_New,
            _lib.AE_AssetMetadata_Delete)


class _AE_AssetLicensors(ctypes.Structure):
    @staticmethod
    def new(client):
        return _SafeObject(
            _lib.AE_AssetLicensors_New,
            _lib.AE_AssetLicensors_Delete)


def _load_lib():
    name = ctypes.util.find_library("aesdk")

    try:
        lib = ctypes.CDLL(name)
    except Exception:
        raise RuntimeError('failed to load native library')

    # AE_Status
    lib.AE_Status_New.argtypes = []
    lib.AE_Status_New.restype = ctypes.POINTER(_AE_Status)

    lib.AE_Status_Delete.argtypes = [
        ctypes.POINTER(ctypes.POINTER(_AE_Status))]
    lib.AE_Status_Delete.restype = None

    lib.AE_Status_OK.argtypes = [ctypes.POINTER(_AE_Status)]
    lib.AE_Status_OK.restype = ctypes.c_bool

    lib.AE_Status_GetCode.argtypes = [ctypes.POINTER(_AE_Status)]
    lib.AE_Status_GetCode.restype = ctypes.c_int

    lib.AE_Status_GetMessage.argtypes = [ctypes.POINTER(_AE_Status)]
    lib.AE_Status_GetMessage.restype = ctypes.c_char_p

    # AE_Buffer
    lib.AE_Buffer_New.argtypes = []
    lib.AE_Buffer_New.restype = ctypes.POINTER(_AE_Buffer)

    lib.AE_Buffer_Delete.argtypes = [
        ctypes.POINTER(ctypes.POINTER(_AE_Buffer))]
    lib.AE_Buffer_Delete.restype = None

    lib.AE_Buffer_Set.argtypes = [
        ctypes.POINTER(_AE_Buffer),
        ctypes.c_void_p,
        ctypes.c_size_t]
    lib.AE_Buffer_Set.restype = None

    # AE_Fingerprint
    lib.AE_Fingerprint_New.argtypes = []
    lib.AE_Fingerprint_New.restype = ctypes.POINTER(_AE_Fingerprint)

    lib.AE_Fingerprint_Delete.argtypes = [
        ctypes.POINTER(ctypes.POINTER(_AE_Fingerprint))]
    lib.AE_Fingerprint_Delete.restype = None

    lib.AE_Fingerprint_FromFile.argtypes = [
        ctypes.POINTER(_AE_Fingerprint),
        ctypes.c_char_p,
        ctypes.POINTER(_AE_Status)]
    lib.AE_Fingerprint_FromFile.restype = None

    lib.AE_Fingerprint_FromBuffer.argtypes = [
        ctypes.POINTER(_AE_Fingerprint),
        ctypes.POINTER(_AE_Buffer),
        ctypes.POINTER(_AE_Status)]
    lib.AE_Fingerprint_FromBuffer.restype = None

    # AE_Client
    lib.AE_Client_New.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    lib.AE_Client_New.restype = ctypes.POINTER(_AE_Client)

    lib.AE_Client_Delete.argtypes = [
        ctypes.POINTER(ctypes.POINTER(_AE_Client))]
    lib.AE_Client_Delete.restype = None

    # AE_MetadataSearch
    lib.AE_MetadataSearch_New.argtypes = [ctypes.POINTER(_AE_Client)]
    lib.AE_MetadataSearch_New.restype = ctypes.POINTER(_AE_MetadataSearch)

    lib.AE_MetadataSearch_Delete.argtypes = [
        ctypes.POINTER(ctypes.POINTER(_AE_MetadataSearch))]
    lib.AE_MetadataSearch_Delete.restype = None

    lib.AE_MetadataSearch_Do.argtypes = [
        ctypes.POINTER(_AE_MetadataSearch),
        ctypes.POINTER(_AE_MetadataSearchRequest),
        ctypes.POINTER(_AE_MetadataSearchResult),
        ctypes.POINTER(_AE_Status)]
    lib.AE_MetadataSearch_Do.restype = None

    # AE_MetadataSearchRequest
    lib.AE_MetadataSearchRequest_New.argtypes = []
    lib.AE_MetadataSearchRequest_New.restype = ctypes.POINTER(_AE_MetadataSearchRequest)

    lib.AE_MetadataSearchRequest_Delete.argtypes = [
        ctypes.POINTER(ctypes.POINTER(_AE_MetadataSearchRequest))]
    lib.AE_MetadataSearchRequest_Delete.restype = None

    lib.AE_MetadataSearchRequest_SetFingerprint.argtypes = [
        ctypes.POINTER(_AE_MetadataSearchRequest),
        ctypes.POINTER(_AE_Fingerprint)]
    lib.AE_MetadataSearchRequest_SetFingerprint.restype = None

    # AE_MetadataSearchResult
    lib.AE_MetadataSearchResult_New.argtypes = []
    lib.AE_MetadataSearchResult_New.restype = ctypes.POINTER(_AE_MetadataSearchResult)

    lib.AE_MetadataSearchResult_Delete.argtypes = [
        ctypes.POINTER(ctypes.POINTER(_AE_MetadataSearchResult))]
    lib.AE_MetadataSearchResult_Delete.restype = None

    lib.AE_MetadataSearchResult_GetLookupID.argtypes = [
        POINTER(ctypes.POINTER(_AE_MetadataSearchResult)]
    lib.AE_MetadataSearchResult_GetLookupID.restype = ctypes.c_uint64

    lib.AE_MetadataSearchResult_GetCompletedAt.argtypes = [
        ctypes.POINTER(_AE_MetadataSearchResult)]
    lib.AE_MetadataSearchResult_GetCompletedAt.restype = ctypes.c_uint64

    lib.AE_MetadataSearchResult_NextMatch.argtypes = [
        ctypes.POINTER(_AE_MetadataSearchResult),
        ctypes.POINTER(_AE_MetadataSearchMatch),
        ctypes.POINTER(ctypes.size_t)]
    lib.AE_MetadataSearchResult_NextMatch.restype = ctypes.c_bool

    # AE_MetadataSearchMatch
    lib.AE_MetadataSearchMatch_New.argtypes = []
    lib.AE_MetadataSearchMatch_New.restype = ctypes.POINTER(_AE_MetadataSearchMatch)

    lib.AE_MetadataSearchMatch_Delete.argtypes = [
        ctypes.POINTER(ctypes.POINTER(_AE_MetadataSearchMatch))]
    lib.AE_MetadataSearchMatch_Delete.restype = None

    lib.AE_MetadataSearchMatch_GetAssetID.argtypes = [
        ctypes.POINTER(_AE_MetadataSearchMatch)]
    lib.AE_MetadataSearchMatch_GetAssetID.restype = ctypes.c_uint64

    lib.AE_MetadataSearchMatch_GetAssetType.argtypes = [
        ctypes.POINTER(_AE_MetadataSearchMatch)]
    lib.AE_MetadataSearchMatch_GetAssetType.restype = ctypes.c_int

    lib.AE_MetadataSearchMatch_NextSegment.argtypes = [
        ctypes.POINTER(_AE_MetadataSearchMatch),
        ctypes.POINTER(ctypes.c_int64),
        ctypes.POINTER(ctypes.c_int64),
        ctypes.POINTER(ctypes.c_int64),
        ctypes.POINTER(ctypes.c_int64),
        ctypes.POINTER(ctypes.size_t)]
    lib.AE_MetadataSearchMatch.restype = ctypes.c_bool

    # AE_AssetLibrary
    lib.AE_AssetLibrary_New.argtypes = [ctypes.POINTER(_AE_Client)]
    lib.AE_AssetLibrary_New.restype = ctypes.POINTER(_AE_AssetLibrary)

    lib.AE_AssetLibrary_Delete.argtypes = [
        ctypes.POINTER(ctypes.POINTER(_AE_AssetLibrary))]
    lib.AE_AssetLibrary_Delete.restype = None

    lib.AE_AssetLibrary_Do.argtypes = [
        ctypes.POINTER(_AE_AssetLibrary),
        ctypes.c_uint64,
        ctypes.POINTER(_AE_Asset),
        ctypes.POINTER(_AE_Status)]
    lib.AE_AssetLibrary_Do.restype = None

    # AE_Asset
    lib.AE_Asset_New.argtypes = []
    lib.AE_Asset_New.restype = ctypes.POINTER(_AE_Asset)

    lib.AE_Asset_Delete.argtypes = [ctypes.POINTER(ctypes.POINTER(_AE_Asset))]
    lib.AE_Asset_Delete.restype = None

    lib.AE_Asset_GetMetadata.argtypes = [
        ctypes.POINTER(ctypes.POINTER(_AE_Asset)),
        ctypes.POINTER(ctypes.POINTER(_AE_AssetMetadata))]
    lib.AE_Asset_GetMetadata.restype = None

    # AE_AssetMetadata
    lib.AE_AssetMetadata_New.argtypes = []
    lib.AE_AssetMetadata_New.restype = ctypes.POINTER(_AE_AssetMetadata)

    lib.AE_AssetMetadata_Delete.argtypes = [ctypes.POINTER(ctypes.POINTER(_AE_AssetMetadata))]
    lib.AE_AssetMetadata_Delete.restype = None

    lib.AE_AssetMetadata_GetISRC.argtypes = [
            ctypes.POINTER(ctypes.POINTER(_AE_AssetMetadata))]
    lib.AE_AssetMetadata_GetISRC.restype = ctypes.c_char_p

    lib.AE_AssetMetadata_GetTitle.argtypes = [
            ctypes.POINTER(ctypes.POINTER(_AE_AssetMetadata))]
    lib.AE_AssetMetadata_GetTitle.restype = ctypes.c_char_p

    lib.AE_AssetMetadata_NextArtist.argtypes = [
        ctypes.POINTER(ctypes.POINTER(_AE_AssetMetadata)),
        ctypes.POINTER(ctypes.c_char_p),
        ctypes.POINTER(ctypes.size_t)]
    lib.AE_AssetMetadata_NextArtist.restype = ctypes.c_bool

    lib.AE_AssetMetadata_NextUPC.argtypes = [
        ctypes.POINTER(ctypes.POINTER(_AE_AssetMetadata)),
        ctypes.POINTER(ctypes.c_char_p),
        ctypes.POINTER(ctypes.size_t)]
    lib.AE_AssetMetadata_NextUPC.restype = ctypes.c_bool

    lib.AE_AssetMetadata_NextLicensors.argtypes = [
        ctypes.POINTER(ctypes.POINTER(_AE_AssetMetadata)),
        ctypes.POINTER(_AE_AssetLicensors),
        ctypes.POINTER(ctypes.size_t)]
    lib.AE_AssetMetadata_NextLicensors.restype = ctypes.c_bool

    # AE_AssetLicensors
    lib.AE_AssetLicensors_New.argtypes = []
    lib.AE_AssetLicensors_New.restype = ctypes.POINTER(_AE_AssetLicensors)

    lib.AE_AssetLicensors_Delete.argtypes = [ctypes.POINTER(ctypes.POINTER(_AE_AssetLicensors))]
    lib.AE_AssetLicensors_Delete.restype = None

    lib.AE_AssetLicensors_GetTerritory.argtypes = [
            ctypes.POINTER(ctypes.POINTER(_AE_AssetLicensors))]
    lib.AE_AssetLicensors_GetTerritory.restype = ctypes.c_char_p

    lib.AE_AssetLicensors_NextLicensor.argtypes = [
        ctypes.POINTER(ctypes.POINTER(_AE_AssetLicensors)),
        ctypes.POINTER(_AE_AssetLicensors),
        ctypes.POINTER(ctypes.c_char_p)]
    lib.AE_AssetLicensors_NextLicensor.restype = ctypes.c_bool

    return lib


_lib = _load_lib()
