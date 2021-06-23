ROS
================================================

Here are details for usage of the Blueprint lab ROS1 Packages

Installation
---------------------
To install ROS please follow instructions at http://wiki.ros.org/ROS/Installation.

First clone the repository to your workspace

.. code-block:: bash

   cd ~/catkin_ws/src
   git clone https://github.com/blueprint-lab/Blueprint_Lab_Software.git

Now install the bplprotocol python package

.. code-block:: bash

   cd Blueprint_Lab_Software/bplprotocol
   pip install .

To build all packages

.. code-block:: bash

   cd ~/catkin_ws
   catkin_make

Usage
---------------------------
The ROS Folder is split into several ROS packages.

bpl_passthrough
^^^^^^^^^^^^^^^^^^^^^^^^
The BPL Passthrough is the core package that allows communication to bpl products.
You can connect to a manipulator via serial or UDP (Bravo arms only).
The `bpl_msgs/Packet` data field is structured as a list of uint8. This is a list of bytes.
For incoming floats, they will be encoded as 4 bytes. Refer to the bplprotocol SDK on how to decode these bytes into floats.

.. code-block:: bash

   roslaunch bpl_passthrough udp_passthrough.launch

or

.. code-block:: bash

   roslaunch bpl_passthrough serial_passthrough.launch

Published Topics
""""""""""""""""""""""
`/rx` (`bpl_msgs/Packet`) - Received Packets from the manipulator


Subscribed Topics
""""""""""""""""""""""
`/tx` (`bpl_msgs/Packet`) - Packets that will be sent to the manipulator

Parameters - udp_passthrough.py
"""""""""""""""""""""""""""""""""""""""""""""""""

`ip_address` (string) - IP Address of the arm. (Defaults to 192.168.2.3)

`port` (int) - UDP Port of the arm. (Defaults to 6789)


Parameters - serial_passthrough.py
"""""""""""""""""""""""""""""""""""""""""""""""""
`serial_port` (string) - Serial Port to connect to the arm (Defaults to "/dev/ttyUSB0")

`baudrate` (int) - UDP Port of the arm. (Defaults to 115200)


bpl_alpha_description
^^^^^^^^^^^^^^^^^^^^^^^^

The BPL Alpha Description package contains the Universal Robot Description File (URDF) files of the alpha range of manipulators.

To view an Alpha 5 urdf:

.. code-block:: bash

   roslaunch bpl_alpha_description view_urdf.launch