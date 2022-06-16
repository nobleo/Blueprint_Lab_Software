from setuptools import setup

package_name = 'bpl_passthrough'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='johnsumskas',
    maintainer_email='john@sumskas.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'serial_passthrough = bpl_passthrough.serial_passthrough:main',
            'udp_passthrough = bpl_passthrough.udp_passthrough:main',
            'request_joint_positions = bpl_passthrough.request_joint_positions:main',
            'request_km_end_pos = bpl_passthrough.request_km_end_pos:main'
        ],
    },
)
