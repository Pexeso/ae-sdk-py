User guide
==========

Welcome to the user guide for Python bindings for the Attribution Engine SDK. If you don't have the core library installed yet, see the `installation guide <https://docs.ae.pex.dev/getting-started/installation/>`_ for instructions on how to install it. You can find instructions on how to install the python bindings on `this page guide <https://docs.ae.pex.dev/getting-started/python/>`_.

Fingerprinting
--------------

A fingerprint is how the SDK identifies a piece of digital content. It can be
generated from a media file or from a memory buffer. The content must be
encoded in one of the supported formats and must be longer than 1 second.

Supported formats: 

:Audio: aac
:Video: h264, h265

Example:

.. code-block:: python

    from pexae import Fingerprint
    from base64 import b64encode

    # will raise pexae.AEError on failure
    ft = Fingerprint.from_file("/path/to/file.mp4")
    print(b64encode(ft.dump()))

.. warning::

    Keep in mind that generating a fingerprint is CPU bound operation and might
    consume a significant amount of your CPU time.

    
**API reference**

.. autoclass:: pexae.Fingerprint
   :members:


Client
------

In order to do anything that communicates with the backend service, e.g.
performing a search or retrieving information about an asset, you first need to
initialize a client and authenticate:

.. code-block:: python

    try:
        client = pexae.Client("__client__", "__client__")
    except pexae.AEError:
        # handle error


**API reference**

.. autoclass:: pexae.Client
   :members:


Asset library
-------------

The asset library is used for retrieving information about assets:

.. code-block:: python

    try:
        asset = client.asset_library.get_asset(asset_id)
        print("retrieved info about: {}".format(asset.metadata.title))
    except pexae.AEError:
        # handle error


**API reference**

.. autoclass:: pexae.Asset()
   :members:
.. autoclass:: pexae.AssetType()
   :members:
.. autoclass:: pexae.AssetLibrary()
   :members:
.. autoclass:: pexae.AssetMetadata()
   :members:
      
   
Metadata search
---------------

Now that the client is initialized and authenticated, you can start making
metadata search requests:

.. code-block:: python

    req = pexae.MetadataSearchRequest(fingerprint=ft)
    try:
        res = client.metadata_search.do(req)
        print("lookup {} returned {} matches".format(res.lookup_id, len(res.matches)))
    except pexae.AEError:
        # handle error


**API reference**

.. autoclass:: pexae.MetadataSearch()
   :members:
.. autoclass:: pexae.MetadataSearchRequest
   :members:
.. autoclass:: pexae.MetadataSearchResult()
   :members:
.. autoclass:: pexae.MetadataSearchMatch()
   :members:
