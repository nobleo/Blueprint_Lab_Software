BPL Protocol
========================

Welcome to the BPL Protocol Documentation

Python Installation
-------------------

Here are instructions to install for python

.. code-block:: bash

   cd ./bplprotocol
   pip install .

Usage
-----------------------

.. code-block:: python

    from bplprotocol import BPLProtocol, PacketID

    # Encode a velocity command packet:
    # velocity of +3.0 mm/s to device 0x01 (Jaws)
    data_bytes = BPLProtocol.encode_packet(0x01, PacketID.VELOCITY, BPLProtocol.encode_floats([3.0]))

SDK
--------------------------
.. toctree::
    :maxdepth: 3

    sdk