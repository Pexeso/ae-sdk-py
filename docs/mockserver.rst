.. _client:

################################################################################
Mockserver
################################################################################

Mockserver is a testing server preloaded with some test data that will help you
write, debug and test your applications. The :meth:`Mockserver.new_client`
static method initializes a new client that will use the mockserver for all
communication.

More information can be found in the official `Mockserver documentation`_.

.. _Mockserver documentation: https://docs.ae.pex.com/mockserver/

.. code-block:: python

    try:
        client = pexae.Mockserver.new_client("client01", "secret01")
    except pexae.AEError as err:
        pass  # handle error


********************************************************************************
API reference
********************************************************************************

.. autoclass:: pexae.Mockserver
   :members:
