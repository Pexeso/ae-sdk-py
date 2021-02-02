[![docs](https://img.shields.io/badge/docs-reference-blue.svg)](https://docs.ae.pex.com/python/)
[![Language](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

# Attribution Engine SDK for Python

Python bindings for the [Attribution Engine SDK](https://docs.ae.pex.com).

### Installation

You can install the Python language bindings like this:

```
python3 -m venv env
. env/bin/activate
pip install git+https://github.com/Pexeso/ae-sdk-py.git
```


### Fingerprinting

A fingerprint is how the SDK identifies a piece of digital content.
It can be generated from a media file or from a memory buffer. The
content must be encoded in one of the supported formats and must be
longer than 1 second.

You can generate a fingerprint from a media file:

```python
import pexae

try:
    ft = pexae.Fingerprint.from_file("/path/to/file.mp4")
    # ...
except pexae.AEError as err:
    pass  # handle error
```

Or you can generate a fingerprint from a memory buffer:

```python
import pexae

try:
    with open("/path/to/file.mp4", "rb") as fp:
        ft = pexae.Fingerprint.from_buffer(fp.read())
    # ...
except pexae.AEError as err:
    pass  # handle error
```

Both the files and the memory buffers must be valid media content in
following formats:

```
Audio: aac
Video: h264, h265
```

**Important!** Keep in mind that generating a fingerprint is CPU bound
operation and might consume a significant amount of your CPU time.

Once a fingerprint is created, it can be serialized so that it can be stored in
a database or sent over a network and then subsequently deserialized:

```python
b = ft.dump()
newft = pexae.Fingerprint.load(b)
```


### Metadata search

After the fingerprint is generated, you can use it to perform a metadata search.

```python
req = pexae.MetadataSearchRequest(fingerprint=ft)
try:
    future = client.metadata_search.start(req)
    # do something else in the meantime
    res = future.get()
    print("lookup {} returned {} matches".format(res.lookup_id, len(res.matches)))
except pexae.AEError as err:
    pass  # handle error
```


### License search

Performing a license search is very similar to metadata search.


```python
req = pexae.LicenseSearchRequest(fingerprint=ft)
try:
    fut = client.license_search.start(req)
    # do something else in the meantime
    res = fut.get()
    blocked = res.policies.get('US') == pexae.BasicPolicy.BLOCK
    print("blocked in US: {}".format(blocked))
except pexae.AEError as err:
    pass  # handle error
```

The most significant difference between the searches currently is in the
results they return. See MetadataSearchResult and LicenseSearchResult for
more information.


### Asset library

You can use AssetLibrary to retrieve information about matched assets.

```python
try:
    asset = client.asset_library.get_asset(asset_id)
    print("retrieved info about: {}".format(asset.metadata.title))
except pexae.AEError as err:
    pass  # handle error
```
