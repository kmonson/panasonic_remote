# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='panasonic-remote',
    version='1.0.0',
    description='Zoom remote control for Panasonic HC-W580 camcorder',
    url='https://github.com/kmonson/panasonic_remote',
    author='Kyle Monson',
    python_requires='>=3.7, <4',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=['PySide2>=5.14.1'],
    extras_require={
        'dev': ['pyqt5-tools>=5.13.2'],
    },
    entry_points={
        'console_scripts': [
            'panasonic-remote=camera_controller.__main__:main',
        ],
    }
)
