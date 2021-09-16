ROS1 Drivers
=====================

Here are details for usage of the Blueprint lab ROS1 Packages

Installation
---------------------
To install ROS please follow instructions at http://wiki.ros.org/ROS/Installation.

First clone the repository to your workspace

.. code-block:: bash

   cd ~/catkin_workspace/src
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

