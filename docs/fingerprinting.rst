###############################################################################
Fingerprinting
###############################################################################

A fingerprint is how the SDK identifies a piece of digital content. It can be
generated from a media file or from a memory buffer. The content must be
encoded in one of the supported formats and must be longer than 1 second.

Supported formats:

:Audio: aac
:Video: h264, h265

Example (creating a fingerprint from a file):

.. code-block:: python

    import pexae

    try:
        ft = pexae.Fingerprint.from_file("/path/to/file.mp4")
        # ...
    except pexae.AEError as err:
        pass  # handle error

Example (creating a fingerprint from a byte buffer):

.. code-block:: python

    import pexae

    try:
        with open("/path/to/file.mp4", "rb") as fp:
            ft = pexae.Fingerprint.from_buffer(fp.read())
        # ...
    except pexae.AEError as err:
        pass  # handle error

.. warning::

    Keep in mind that generating a fingerprint is a CPU bound operation and might
    consume a significant amount of your CPU time.

Once a fingerprint is created, it can be serialized so that it can be stored in
a database or sent over a network and then subsequently deserialized:

.. code-block:: python

    b = ft.dump()
    newft = pexae.Fingerprint.load(b)


*******************************************************************************
API reference
*******************************************************************************

.. autoclass:: pexae.Fingerprint()

