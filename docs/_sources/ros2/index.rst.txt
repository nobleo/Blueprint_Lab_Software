ROS2
================================================

Here are details for usage of the Blueprint lab ROS2 Packages

Installation
---------------------
To install ROS please follow instructions at https://docs.ros.org/en/foxy/Installation.html.

First clone the repository to your workspace. 

.. code-block:: bash

   cd ~/dev_ws/src
   git clone https://github.com/blueprint-lab/Blueprint_Lab_Software.git


Now install the bplprotocol python package

.. code-block:: bash

   cd Blueprint_Lab_Software/bplprotocol
   pip3 install .

To build all packages

.. code-block:: bash

   cd ~/dev_ws
   colcon build


Usage
---------------------------
The ROS2 Folder is split into several ROS2 packages.

bpl_passthrough
^^^^^^^^^^^^^^^^^^^^^^^^
The BPL Passthrough is the core package that allows communication to bpl products.
You can connect to a manipulator via serial or UDP (Bravo arms only).
The :code:`bpl_msgs/Packet` data field is structured as a list of uint8. This is a list of bytes.
For incoming floats, they will be encoded as 4 bytes. Refer to the bplprotocol SDK on how to decode these bytes into floats.


bpl_bravo_description
^^^^^^^^^^^^^^^^^^^^^^^^


bpl_bringup
^^^^^^^^^^^^^^^^^^^^^^^^

