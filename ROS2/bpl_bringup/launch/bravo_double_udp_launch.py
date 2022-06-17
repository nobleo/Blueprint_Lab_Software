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
    urdf_file_name = 'urdf/bravo_double_example.urdf.xacro'
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
                "joint_names":['bravo_b_axis_a', 'bravo_b_axis_b', 'bravo_b_axis_c', 'bravo_b_axis_d', 'bravo_b_axis_e'],
                'request_frequency':10,
                'publish_frequency': 20,
            }],
            namespace="bravo_b"
        ),

        Node(
            package='bpl_control',
            executable='control_node',
            namespace="bravo_b"
        ),

        Node(
            package='bpl_control',
            executable='b5_gui',
            namespace="bravo_b"
        ),

     
        
        Node(package='bpl_passthrough',
            executable='udp_passthrough',
            parameters=[{"ip_address":"192.168.2.3"}],
            namespace="bravo_b"),
        Node(
            package='bpl_passthrough',
            executable='request_km_end_pos',
            namespace="bravo_b",
            parameters=[{"frame_id": 'bravo_b_base_link'}]
        ),


        Node(
            package='bpl_control',
            executable='joint_state_publisher',
            parameters=[{
                "joints":[1, 2, 3, 4, 5, 6, 7],
                "joint_names":['bravo_a_axis_a', 'bravo_a_axis_b', 'bravo_a_axis_c', 'bravo_a_axis_d', 'bravo_a_axis_e', 'bravo_a_axis_f', 'bravo_a_axis_g'],
                'request_frequency':10,
                'publish_frequency': 20,
            }],
            namespace="bravo_a"
        ),

        Node(
            package='bpl_control',
            executable='control_node',
            parameters=[{
                "joints":[1, 2, 3, 4, 5, 6, 7]}],
            namespace="bravo_a"
        ),

        Node(
            package='bpl_control',
            executable='b7_gui',
            namespace="bravo_a"
        ),

        
        Node(package='bpl_passthrough',
            executable='udp_passthrough',
            parameters=[{"ip_address":"192.168.2.7"}],
            namespace="bravo_a"),

        Node(
            package='bpl_passthrough',
            executable='request_km_end_pos',
            namespace="bravo_a",
            parameters=[{"frame_id": 'bravo_a_base_link'}]
        ),

        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            parameters=[{"source_list": ["bravo_b/joint_states", "bravo_a/joint_states"
            ]}]),

       


        Node(
            package='rviz2',
            executable='rviz2',
            name='RVIZ',
            arguments=['-d', rviz_config_file],
        )
    ])