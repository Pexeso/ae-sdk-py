# Copyright 2020 Pexeso Inc. All rights reserved.

import os
import ctypes
import ctypes.util
import os


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
    def new(lib):
        return _SafeObject(lib.AE_Status_New, lib.AE_Status_Delete)


class _AE_Buffer(ctypes.Structure):
    @staticmethod
    def new(lib):
        return _SafeObject(lib.AE_Buffer_New, lib.AE_Buffer_Delete)


class _AE_Fingerprint(ctypes.Structure):
    @staticmethod
    def new(lib):
        return _SafeObject(lib.AE_Fingerprint_New, lib.AE_Fingerprint_Delete)


class _AE_Client(ctypes.Structure):
    @staticmethod
    def new(lib):
        return _SafeObject(lib.AE_Client_New, lib.AE_Client_Delete)


class _AE_LicenseSearch(ctypes.Structure):
    @staticmethod
    def new(lib, client):
        return _SafeObject(
            lib.AE_LicenseSearch_New,
            lib.AE_LicenseSearch_Delete,
            args=[client])


class _AE_LicenseSearchFuture(ctypes.Structure):
    @staticmethod
    def new(lib):
        return _SafeObject(
            lib.AE_LicenseSearchFuture_New,
            lib.AE_LicenseSearchFuture_Delete)


class _AE_LicenseSearchRequest(ctypes.Structure):
    @staticmethod
    def new(lib):
        return _SafeObject(
            lib.AE_LicenseSearchRequest_New,
            lib.AE_LicenseSearchRequest_Delete)


class _AE_LicenseSearchResult(ctypes.Structure):
    @staticmethod
    def new(lib):
        return _SafeObject(
            lib.AE_LicenseSearchResult_New,
            lib.AE_LicenseSearchResult_Delete)


class _AE_MetadataSearch(ctypes.Structure):
    @staticmethod
    def new(lib, client):
        return _SafeObject(
            lib.AE_MetadataSearch_New,
            lib.AE_MetadataSearch_Delete,
            args=[client])


class _AE_MetadataSearchFuture(ctypes.Structure):
    @staticmethod
    def new(lib):
        return _SafeObject(
            lib.AE_MetadataSearchFuture_New,
            lib.AE_MetadataSearchFuture_Delete)


class _AE_MetadataSearchRequest(ctypes.Structure):
    @staticmethod
    def new(lib):
        return _SafeObject(
            lib.AE_MetadataSearchRequest_New,
            lib.AE_MetadataSearchRequest_Delete)


class _AE_MetadataSearchResult(ctypes.Structure):
    @staticmethod
    def new(lib):
        return _SafeObject(
            lib.AE_MetadataSearchResult_New,
            lib.AE_MetadataSearchResult_Delete)


class _AE_MetadataSearchMatch(ctypes.Structure):
    @staticmethod
    def new(lib):
        return _SafeObject(
            lib.AE_MetadataSearchMatch_New,
            lib.AE_MetadataSearchMatch_Delete)


class _AE_AssetLibrary(ctypes.Structure):
    @staticmethod
    def new(lib, client):
        return _SafeObject(
            lib.AE_AssetLibrary_New,
            lib.AE_AssetLibrary_Delete,
            args=[client])


class _AE_Asset(ctypes.Structure):
    @staticmethod
    def new(lib):
        return _SafeObject(lib.AE_Asset_New, lib.AE_Asset_Delete)


class _AE_AssetMetadata(ctypes.Structure):
    @staticmethod
    def new(lib):
        return _SafeObject(
            lib.AE_AssetMetadata_New,
            lib.AE_AssetMetadata_Delete)


class _AE_AssetLicensors(ctypes.Structure):
    @staticmethod
    def new(lib):
        return _SafeObject(
            lib.AE_AssetLicensors_New,
            lib.AE_AssetLicensors_Delete)


def _load_lib():
    if os.getenv('PEXAE_NO_CORE_LIB') is not None:
        # Defining PEXAE_NO_CORE_LIB makes this wrapper module import-able even without the shared library.
        # Useful for generating documentation.
        return ctypes.CDLL(None)

    name = ctypes.util.find_library("pexae")
    if name is None:
        raise RuntimeError('failed to find native library')

    try:
        lib = ctypes.CDLL(name)
    except Exception:
        raise RuntimeError('failed to load native library')

    # AE_Init
    lib.AE_Init.argtypes = [ctypes.POINTER(_AE_Status)]
    lib.AE_Init.restype = None

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

    lib.AE_Buffer_GetData.argtypes = [ctypes.POINTER(_AE_Buffer)]
    lib.AE_Buffer_GetData.restype = ctypes.c_void_p

    lib.AE_Buffer_GetSize.argtypes = [ctypes.POINTER(_AE_Buffer)]
    lib.AE_Buffer_GetSize.restype = ctypes.c_size_t

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
    lib.AE_Client_New.argtypes = []
    lib.AE_Client_New.restype = ctypes.POINTER(_AE_Client)

    lib.AE_Client_Delete.argtypes = [
        ctypes.POINTER(ctypes.POINTER(_AE_Client))]
    lib.AE_Client_Delete.restype = None

    lib.AE_Client_Init.argtypes = [
        ctypes.POINTER(_AE_Client),
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.POINTER(_AE_Status)]
    lib.AE_Client_Init.restype = None

    # AE_LicenseSearch
    lib.AE_LicenseSearch_New.argtypes = [ctypes.POINTER(_AE_Client)]
    lib.AE_LicenseSearch_New.restype = ctypes.POINTER(_AE_LicenseSearch)

    lib.AE_LicenseSearch_Delete.argtypes = [
        ctypes.POINTER(ctypes.POINTER(_AE_LicenseSearch))]
    lib.AE_LicenseSearch_Delete.restype = None

    lib.AE_LicenseSearch_Start.argtypes = [
        ctypes.POINTER(_AE_LicenseSearch),
        ctypes.POINTER(_AE_LicenseSearchRequest),
        ctypes.POINTER(_AE_LicenseSearchFuture),
        ctypes.POINTER(_AE_Status)]
    lib.AE_LicenseSearch_Start.restype = None

    # AE_LicenseSearchFuture
    lib.AE_LicenseSearchFuture_New.argtypes = []
    lib.AE_LicenseSearchFuture_New.restype = ctypes.POINTER(_AE_LicenseSearchFuture)

    lib.AE_LicenseSearchFuture_Delete.argtypes = [
        ctypes.POINTER(ctypes.POINTER(_AE_LicenseSearchFuture))]
    lib.AE_LicenseSearchFuture_Delete.restype = None

    lib.AE_LicenseSearchFuture_Get.argtypes = [
        ctypes.POINTER(_AE_LicenseSearchFuture),
        ctypes.POINTER(_AE_LicenseSearchResult),
        ctypes.POINTER(_AE_Status)]
    lib.AE_LicenseSearchFuture_Get.restype = None

    # AE_LicenseSearchRequest
    lib.AE_LicenseSearchRequest_New.argtypes = []
    lib.AE_LicenseSearchRequest_New.restype = ctypes.POINTER(_AE_LicenseSearchRequest)

    lib.AE_LicenseSearchRequest_Delete.argtypes = [
        ctypes.POINTER(ctypes.POINTER(_AE_LicenseSearchRequest))]
    lib.AE_LicenseSearchRequest_Delete.restype = None

    lib.AE_LicenseSearchRequest_SetFingerprint.argtypes = [
        ctypes.POINTER(_AE_LicenseSearchRequest),
        ctypes.POINTER(_AE_Fingerprint)]
    lib.AE_LicenseSearchRequest_SetFingerprint.restype = None

    # AE_LicenseSearchResult
    lib.AE_LicenseSearchResult_New.argtypes = []
    lib.AE_LicenseSearchResult_New.restype = ctypes.POINTER(_AE_LicenseSearchResult)

    lib.AE_LicenseSearchResult_Delete.argtypes = [
        ctypes.POINTER(ctypes.POINTER(_AE_LicenseSearchResult))]
    lib.AE_LicenseSearchResult_Delete.restype = None

    lib.AE_LicenseSearchResult_GetLookupID.argtypes = [
        ctypes.POINTER(_AE_LicenseSearchResult)]
    lib.AE_LicenseSearchResult_GetLookupID.restype = ctypes.c_uint64

    lib.AE_LicenseSearchResult_GetCompletedAt.argtypes = [
        ctypes.POINTER(_AE_LicenseSearchResult)]
    lib.AE_LicenseSearchResult_GetCompletedAt.restype = ctypes.c_uint64

    lib.AE_LicenseSearchResult_NextPolicy.argtypes = [
        ctypes.POINTER(_AE_LicenseSearchResult),
        ctypes.POINTER(ctypes.c_char_p),
        ctypes.POINTER(ctypes.c_int),
        ctypes.POINTER(ctypes.c_size_t)]
    lib.AE_LicenseSearchResult_NextPolicy.restype = ctypes.c_bool

    # AE_MetadataSearch
    lib.AE_MetadataSearch_New.argtypes = [ctypes.POINTER(_AE_Client)]
    lib.AE_MetadataSearch_New.restype = ctypes.POINTER(_AE_MetadataSearch)

    lib.AE_MetadataSearch_Delete.argtypes = [
        ctypes.POINTER(ctypes.POINTER(_AE_MetadataSearch))]
    lib.AE_MetadataSearch_Delete.restype = None

    lib.AE_MetadataSearch_Start.argtypes = [
        ctypes.POINTER(_AE_MetadataSearch),
        ctypes.POINTER(_AE_MetadataSearchRequest),
        ctypes.POINTER(_AE_MetadataSearchFuture),
        ctypes.POINTER(_AE_Status)]
    lib.AE_MetadataSearch_Start.restype = None

    # AE_MetadataSearch
    lib.AE_MetadataSearchFuture_New.argtypes = []
    lib.AE_MetadataSearchFuture_New.restype = ctypes.POINTER(_AE_MetadataSearchFuture)

    lib.AE_MetadataSearchFuture_Delete.argtypes = [
        ctypes.POINTER(ctypes.POINTER(_AE_MetadataSearchFuture))]
    lib.AE_MetadataSearchFuture_Delete.restype = None

    lib.AE_MetadataSearchFuture_Get.argtypes = [
        ctypes.POINTER(_AE_MetadataSearchFuture),
        ctypes.POINTER(_AE_MetadataSearchResult),
        ctypes.POINTER(_AE_Status)]
    lib.AE_MetadataSearchFuture_Get.restype = None

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
        ctypes.POINTER(_AE_MetadataSearchResult)]
    lib.AE_MetadataSearchResult_GetLookupID.restype = ctypes.c_uint64

    lib.AE_MetadataSearchResult_GetCompletedAt.argtypes = [
        ctypes.POINTER(_AE_MetadataSearchResult)]
    lib.AE_MetadataSearchResult_GetCompletedAt.restype = ctypes.c_uint64

    lib.AE_MetadataSearchResult_NextMatch.argtypes = [
        ctypes.POINTER(_AE_MetadataSearchResult),
        ctypes.POINTER(_AE_MetadataSearchMatch),
        ctypes.POINTER(ctypes.c_size_t)]
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
        ctypes.POINTER(ctypes.c_size_t)]
    lib.AE_MetadataSearchMatch_NextSegment.restype = ctypes.c_bool

    # AE_AssetLibrary
    lib.AE_AssetLibrary_New.argtypes = [ctypes.POINTER(_AE_Client)]
    lib.AE_AssetLibrary_New.restype = ctypes.POINTER(_AE_AssetLibrary)

    lib.AE_AssetLibrary_Delete.argtypes = [
        ctypes.POINTER(ctypes.POINTER(_AE_AssetLibrary))]
    lib.AE_AssetLibrary_Delete.restype = None

    lib.AE_AssetLibrary_GetAsset.argtypes = [
        ctypes.POINTER(_AE_AssetLibrary),
        ctypes.c_uint64,
        ctypes.POINTER(_AE_Asset),
        ctypes.POINTER(_AE_Status)]
    lib.AE_AssetLibrary_GetAsset.restype = None

    # AE_Asset
    lib.AE_Asset_New.argtypes = []
    lib.AE_Asset_New.restype = ctypes.POINTER(_AE_Asset)

    lib.AE_Asset_Delete.argtypes = [ctypes.POINTER(ctypes.POINTER(_AE_Asset))]
    lib.AE_Asset_Delete.restype = None

    lib.AE_Asset_GetMetadata.argtypes = [
        ctypes.POINTER(_AE_Asset),
        ctypes.POINTER(_AE_AssetMetadata)]
    lib.AE_Asset_GetMetadata.restype = None

    # AE_AssetMetadata
    lib.AE_AssetMetadata_New.argtypes = []
    lib.AE_AssetMetadata_New.restype = ctypes.POINTER(_AE_AssetMetadata)

    lib.AE_AssetMetadata_Delete.argtypes = [
        ctypes.POINTER(ctypes.POINTER(_AE_AssetMetadata))]
    lib.AE_AssetMetadata_Delete.restype = None

    lib.AE_AssetMetadata_GetISRC.argtypes = [
        ctypes.POINTER(_AE_AssetMetadata)]
    lib.AE_AssetMetadata_GetISRC.restype = ctypes.c_char_p

    lib.AE_AssetMetadata_GetTitle.argtypes = [
        ctypes.POINTER(_AE_AssetMetadata)]
    lib.AE_AssetMetadata_GetTitle.restype = ctypes.c_char_p

    lib.AE_AssetMetadata_NextArtist.argtypes = [
        ctypes.POINTER(_AE_AssetMetadata),
        ctypes.POINTER(ctypes.c_char_p),
        ctypes.POINTER(ctypes.c_size_t)]
    lib.AE_AssetMetadata_NextArtist.restype = ctypes.c_bool

    lib.AE_AssetMetadata_NextUPC.argtypes = [
        ctypes.POINTER(_AE_AssetMetadata),
        ctypes.POINTER(ctypes.c_char_p),
        ctypes.POINTER(ctypes.c_size_t)]
    lib.AE_AssetMetadata_NextUPC.restype = ctypes.c_bool

    lib.AE_AssetMetadata_NextLicensors.argtypes = [
        ctypes.POINTER(_AE_AssetMetadata),
        ctypes.POINTER(_AE_AssetLicensors),
        ctypes.POINTER(ctypes.c_size_t)]
    lib.AE_AssetMetadata_NextLicensors.restype = ctypes.c_bool

    # AE_AssetLicensors
    lib.AE_AssetLicensors_New.argtypes = []
    lib.AE_AssetLicensors_New.restype = ctypes.POINTER(_AE_AssetLicensors)

    lib.AE_AssetLicensors_Delete.argtypes = [
            ctypes.POINTER(ctypes.POINTER(_AE_AssetLicensors))]
    lib.AE_AssetLicensors_Delete.restype = None

    lib.AE_AssetLicensors_GetTerritory.argtypes = [
        ctypes.POINTER(_AE_AssetLicensors)]
    lib.AE_AssetLicensors_GetTerritory.restype = ctypes.c_char_p

    lib.AE_AssetLicensors_NextLicensor.argtypes = [
        ctypes.POINTER(_AE_AssetLicensors),
        ctypes.POINTER(ctypes.c_char_p),
        ctypes.POINTER(ctypes.c_size_t)]
    lib.AE_AssetLicensors_NextLicensor.restype = ctypes.c_bool

    # Initialize and return the library
    c_status = _AE_Status.new(lib)
    lib.AE_Init(c_status.get())

    if not lib.AE_Status_OK(c_status.get()):
        raise RuntimeError("failed to initialize library")
    return lib


_lib = _load_lib()
