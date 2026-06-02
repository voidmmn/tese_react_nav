import os
from glob import glob

from setuptools import find_packages, setup

package_name = 'tese_nav'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Recursos instalados (acessíveis via ament_index em runtime)
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.sdf')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*')),
        (os.path.join('share', package_name, 'config', 'maps'),
            glob('config/maps/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Milton Miranda Neto',
    maintainer_email='voidmmn@gmail.com',
    description='Bellman atratora + Stay Alert para inspeção de subestações.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'bellman_node = tese_nav.bellman_node:main',
            'stay_alert_node = tese_nav.stay_alert_node:main',
            'anomaly_simulator = tese_nav.anomaly_simulator:main',
            'mission_node = tese_nav.mission_node:main',
            'metrics_node = tese_nav.metrics_node:main',
            'fake_scan_publisher = tese_nav.fake_scan_publisher:main',
        ],
    },
)
