import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.descriptions import ParameterValue

from bplprotocol import PacketReader, BPLProtocol, PacketID



def generate_launch_description():

    desc_pkg_share = get_package_share_directory('bpl_bravo_description')
    urdf_file_name = 'urdf/bravo_5_example.urdf.xacro'
    urdf_path = os.path.join(desc_pkg_share, urdf_file_name)

    rviz_config_file = os.path.join(desc_pkg_share, 'rviz/rviz.rviz')

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': ParameterValue(
            Command(['xacro ', str(urdf_path)]), value_type=str)}]),

        Node(
            package='bpl_control',
            executable='joint_state_publisher',
            parameters=[{
                "joints":[1, 2, 3, 4, 5],
                "joint_names":['bravo_axis_a', 'bravo_axis_b', 'bravo_axis_c', 'bravo_axis_d', 'bravo_axis_e'],
                'request_frequency':10,
                'publish_frequency': 20,
            }]
        ),
        
        Node(package='bpl_passthrough',
            executable='udp_passthrough',
            parameters=[{"ip_address":"192.168.2.156"}]),

        Node(
            package='rviz2',
            executable='rviz2',
            name='RVIZ',
            arguments=['-d', rviz_config_file]
        )
    ])