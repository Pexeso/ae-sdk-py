################################################################################
Asset library
################################################################################

The asset library is used for retrieving information about assets:


.. code-block:: python

    try:
        asset = client.asset_library.get_asset(asset_id)
        print("retrieved info about: {}".format(asset.metadata.title))
    except pexae.AEError as err:
        pass  # handle error


********************************************************************************
API reference
********************************************************************************

.. autoclass:: pexae.AssetType()

.. autoclass:: pexae.AssetMetadata()

.. autoclass:: pexae.Asset()

.. autoclass:: pexae.AssetLibrary()

