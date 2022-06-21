BPL Protocol - C SDK
========================

Welcome to the BPL Protocol Documentation C SDK

Here you can find instructions on how to use the C SDK

The entire BPL Protocol SDK is contained one file header file.

You can find the SDK here: :download:`bplprotocol.h <../../../C/bplprotocol.h>`
Or in the SDK here `C/bplprotocol.h`


Examples
----------------------
Some code examples using the bplprotocol can be found under C/examples

.. toctree::
    :maxdepth: 1

    examples/encoding_packets
    examples/decoding_packets

Running Examples
~~~~~~~~~~~~~~~~~~~~~~
To view the C examples compile them like so.
Replace the example name with the Relevant example you would like to test.


.. code-block:: bash

   cd ./C/examples/
   gcc decodePacketExample.c -I .. -o example_script

   # To run the example
   ./example_script